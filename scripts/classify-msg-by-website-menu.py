#!/usr/bin/env python3
"""依 MSG B2E 實際選單整理 Redmine 需求單。"""

import json
import re
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/sources/msg/redmine/issues_all.json"
MENU = ROOT / "data/sources/msg/website-menus.json"
OUT = ROOT / "docs/msg/requirements"
PAGES_OUT = OUT / "pages"
BASE_URL = "https://redmine.etzone.net/issues"
PROJECT_DOCS_L2 = Path("/home/art/openab-repos/project-docs/projects/MSG/data/business-flows/B2E/L2")
L2_INDEX = PROJECT_DOCS_L2 / "INDEX.md"


# 規則順序代表優先權。標題先判斷，只有標題沒有命中時才讀取需求描述。
# 只把使用者提供的選單頁面列為前台分類；聊天室、Webhook、JOB、LINE 綁定等
# 沒有出現在這份選單的功能，落到「非頁面／共用功能」或「待人工確認頁面」。
RULES = [
    ("AI 費用報表", "/AiCostReport", r"AI\s*費用|AI\s*成本|費用報表|AiCostReport"),
    ("訊息統計資訊", "/MessagesMetrics", r"訊息統計|訊息資料統計|MessagesMetrics|好友統計|每日好友"),
    ("簽到活動管理", "/CheckIn", r"簽到|報到|印章|CheckIn"),
    ("遊戲管理", "/GameManage", r"遊戲|抽獎|刮刮卡|搖搖樂|獎項|GameManage"),
    ("照片合成功能", "/FrameMergeActivity", r"照片合成|合成圖片|同框照|新年圖片|FrameMerge"),
    ("直播設定", "/Stream", r"直播|見面會|直播設定|直播活動|LIFF活動頁|Stream"),
    ("圖庫頁籤管理", "/GalleryManage", r"圖庫頁籤|頁籤管理|GalleryManage"),
    ("圖庫", "/Gallery", r"圖庫|圖片庫|圖庫管理|縮圖|FaceAI|Gallery"),
    ("客戶名單檢查", "/CustomerCheck", r"客戶名單檢查|客戶檢查|CustomerCheck"),
    ("客戶管理", "/Customer", r"客戶管理|修改客戶|客戶資料|客戶手機|會員資料|Customer"),
    ("指派", "/Assign", r"指派|派線|轉接|分配客戶|客服分流|Assign"),
    ("離線訊息管理", "/LeaveMessages", r"離線訊息|離線留言|LeaveMessages"),
    ("商品維護", "/Product", r"商品維護|商品檔案|商品管理|Product"),
    ("圖文選單", "/Richmenu", r"圖文選單|Richmenu"),
    ("對話查詢", "/Dialog", r"對話查詢|歷史紀錄查詢|聊天歷史紀錄查詢|ElasticSearchAPI|Dialog"),
    ("受眾管理", "/Audience", r"受眾|分眾|Audience"),
    ("模板訊息", "/Combo", r"模板|模板訊息|模板設定|模板素材|Combo"),
    ("統計資訊", "/Metrics", r"統計資訊|成效報表|會員統計|統計資料|下載報表|Metrics"),
    ("功能管理", "/Function", r"功能管理|功能權限|Function"),
    ("角色管理", "/Role", r"角色管理|角色設定|角色功能|角色權限|RBAC|Role"),
    ("使用者管理", "/User", r"使用者管理|新增使用者|新增帳號|系統使用者|AD帳號|使用者帳號|使用者狀態|User"),
    ("待確認使用者", "/PendingUser", r"待確認使用者|待確認 User|PendingUser"),
    (
        "非頁面／共用功能",
        "",
        r"API|JOB|排程|Webhook|webhook|Redis|資料庫|DB|SP|SQL|Sonarqube|SonarQube|"
        r"架構|效能|快取|SSO|登入|login|登出|Session|Token|OTP|手機驗證|綁定|LIFF|"
        r"LINE|Line SDK|AI助手|AI 摘要|聊天室|聊天|訊息|SignalR|Hub|Log|LOG|錯誤|"
        r"異常|重構|版本|版號|環境|權限|元件|UI|前端|後端|資料遮蔽|個資|密碼|白名單|網址|"
        r"LDAP|nginx|IP|int\s*溢位|table|欄位|container|appsettings|DAO|Facade|依賴注入|"
        r"FUGO|用戶狀態|事件紀錄|測試框架|電話隱碼|資料表|Controller|Model",
    ),
]


def normalize_route(route):
    route = str(route or "").strip().strip("`").lower().rstrip("/") or "/"
    return route if route.startswith("/") else f"/{route}"


def escape_cell(value):
    return str(value or "").replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def flatten_menu(menu):
    pages = []
    groups = list(enumerate(menu.get("data", [])))
    groups.sort(key=lambda item: (item[1].get("sort", 0), item[0]))
    for group_position, (_, group) in enumerate(groups, 1):
        children = list(enumerate(group.get("childMenus") or []))
        children.sort(key=lambda item: (item[1].get("sort", 0), item[0]))
        for page_position, (_, page) in enumerate(children, 1):
            if page.get("url"):
                pages.append(
                    {
                        "group_id": group.get("id"),
                        "group_name": group.get("name", ""),
                        "group_sort": group.get("sort", 0),
                        "group_order": group_position,
                        "id": page.get("id"),
                        "name": page.get("name", ""),
                        "url": page.get("url", ""),
                        "sort": page.get("sort", 0),
                        "page_order": page_position,
                        "accessLevel": page.get("accessLevel"),
                    }
                )
    return pages


def load_l2_index():
    found = {}
    if not L2_INDEX.exists():
        return found
    for line in L2_INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "路由路徑" in line:
            continue
        columns = [item.strip() for item in line.strip().strip("|").split("|")]
        if len(columns) < 3:
            continue
        route = normalize_route(columns[1])
        match = re.search(r"\]\(([^)]+)\)", columns[2])
        if match:
            found[route] = match.group(1)
    return found


def purpose_from_file(path):
    if not path.exists():
        return "尚未找到 MSG project-docs 的 L2 頁面全貌文件。"
    lines = path.read_text(encoding="utf-8").splitlines()
    for heading in ("## 頁面概覽", "## 頁面意圖描述"):
        try:
            start = lines.index(heading) + 1
        except ValueError:
            continue
        collected = []
        for line in lines[start:]:
            if line.startswith("#") or line.startswith("|"):
                break
            text = line.strip().lstrip("> ")
            if text:
                collected.append(text)
            elif collected:
                break
        if collected:
            return " ".join(collected).replace("|", "\\|")[:360]

    paragraphs = []
    current = []
    for line in lines:
        if line.startswith("#") or line.startswith("|"):
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            continue
        text = line.strip().lstrip("> ")
        if text:
            current.append(text)
        elif current:
            paragraphs.append(" ".join(current).strip())
            current = []
    if current:
        paragraphs.append(" ".join(current).strip())
    purpose = next((item for item in paragraphs if len(item) > 20), "尚未從 L2 文件擷取到用途摘要。")
    return purpose.replace("|", "\\|")[:360]


def classify(issue):
    subject = issue.get("subject", "")
    body = f"{subject} {issue.get('description', '')}"
    for page, url, pattern in RULES:
        if re.search(pattern, subject, re.IGNORECASE):
            return page, url, "標題", pattern
    for page, url, pattern in RULES:
        if re.search(pattern, body, re.IGNORECASE):
            return page, url, "內容", pattern
    return "待人工確認頁面", "", "未命中規則", ""


def file_name(page, menu_page=None):
    safe_page = page.replace("/", "-").replace("／", "-")
    if menu_page:
        return f"{menu_page['group_order']:02d}-{menu_page['page_order']:02d}-{safe_page}.md"
    if page == "非頁面／共用功能":
        return "98-非頁面-共用功能.md"
    return "99-待人工確認頁面.md"


def issue_row(issue, evidence):
    issue_id = issue["id"]
    project = issue.get("project", {}).get("name", "").strip()
    tracker = issue.get("tracker", {}).get("name", "")
    status = issue.get("status", {}).get("name", "")
    assigned = issue.get("assigned_to", {}).get("name", "未指派")
    link = f"[{issue_id}]({BASE_URL}/{issue_id})"
    return (
        f"| {link} | {escape_cell(project)} | {escape_cell(issue.get('subject'))} | "
        f"{escape_cell(tracker)} | {escape_cell(status)} | {escape_cell(assigned)} | "
        f"{issue.get('created_on', '')[:10]} | {evidence['reason']} |"
    )


def write_page_purpose_index(menu_pages, l2):
    lines = [
        "# MSG 網站頁面用途索引",
        "",
        "用途說明來源：`/home/art/openab-repos/project-docs/projects/MSG/data/business-flows/B2E/L2/`。",
        "本文件以 MSG B2E 實際選單為主，補充目前可找到的 L2 頁面全貌文件，作為需求單分類的人工校對依據。",
        "",
        "| 目錄順序 | 頁面順序 | 目錄 | 頁面 | URL | 權限 | 頁面用途摘要 | project-docs L2 |",
        "|---:|---:|---|---|---|---:|---|---|",
    ]
    for page in menu_pages:
        route = page["url"]
        filename = l2.get(normalize_route(route))
        source = f"`{filename}`" if filename else "—"
        purpose = purpose_from_file(PROJECT_DOCS_L2 / filename) if filename else "尚未找到對應 L2 文件，先依 MSG 選單名稱與需求單內容判斷。"
        access = page["accessLevel"] if page["accessLevel"] is not None else "—"
        lines.append(
            f"| {page['group_order']} | {page['page_order']} | {escape_cell(page['group_name'])} | "
            f"{escape_cell(page['name'])} | `{route}` | {access} | {purpose} | {source} |"
        )
    lines += [
        "",
        "## 使用方式",
        "",
        "1. 先以 MSG 選單中的頁面與 URL 判斷需求是否屬於可見功能。",
        "2. 需求單若只有 API、JOB、Webhook、聊天室或 LINE 服務行為，且沒有對應選單頁面，歸入「非頁面／共用功能」。",
        "3. 若需求內容不足以判斷頁面，歸入「待人工確認頁面」，不因單一模糊關鍵字強行分類。",
        "4. 需要完整流程時，沿著 project-docs L2 文件名稱回到 MSG 知識庫查閱。",
    ]
    (OUT / "page-purpose-index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_classification_index(menu_pages, groups, evidence, source_data):
    lines = [
        "# MSG 需求單頁面分類 Index",
        "",
        f"來源需求單：`{SOURCE.relative_to(ROOT)}`",
        f"網站選單：`{MENU.relative_to(ROOT)}`",
        "",
        "## 分類流程",
        "",
        "1. 以 MSG 選單提供的頁面與 URL 作為主要分類架構。",
        "2. 先比對需求單標題，再以標題加需求描述全文補充判斷。",
        "3. 同一張需求單只歸入一個主要分類，保留命中位置與規則於 `website-page-classification.json`。",
        "4. 沒有對應選單頁面的 API、JOB、Webhook、聊天室、LINE 綁定與共用技術內容，歸入「非頁面／共用功能」。",
        "5. 無法可靠判斷時歸入「待人工確認頁面」，不自行猜測。",
        "6. 父選單與子頁面依 JSON 的 `sort` 升冪排列；相同 `sort` 保留 JSON 原始順序，`pages/` 檔名前綴同步反映此層級。",
        "",
        "## 分類結果",
        "",
        f"- 需求單總數：{len(source_data['issues'])}",
        f"- MSG 目錄頁面：{len(menu_pages)}",
        f"- 分類總數：{len(groups)}（含 MSG 目錄頁面、非頁面／共用功能與待人工確認）",
        f"- 非頁面／共用功能：{len(groups.get(('非頁面／共用功能', ''), []))} 筆",
        f"- 待人工確認頁面：{len(groups.get(('待人工確認頁面', ''), []))} 筆",
        "",
        "| 目錄順序 | 頁面順序 | 目錄 | 頁面 | URL | 需求單數 |",
        "|---:|---:|---|---|---|---:|",
    ]
    menu_by_key = {(page["name"], page["url"]): page for page in menu_pages}
    for key, issues in groups.items():
        page, url = key
        menu_page = menu_by_key.get(key)
        group_name = menu_page.get("group_name", "共用／待確認") if menu_page else "共用／待確認"
        group_order = menu_page.get("group_order", "—") if menu_page else "—"
        page_order = menu_page.get("page_order", "—") if menu_page else "—"
        lines.append(
            f"| {group_order} | {page_order} | {escape_cell(group_name)} | {escape_cell(page)} | "
            f"`{url or '—'}` | {len(issues)} |"
        )
    lines += [
        "",
        "## 規則維護",
        "",
        "分類規則位於 `scripts/classify-msg-by-website-menu.py`。若 MSG 目錄新增或修改頁面，先更新 `data/sources/msg/website-menus.json`，再補上規則並重新產生本索引、用途索引與 `pages/` 清單。",
        "",
        "每一頁的需求明細位於本目錄 `pages/`；分類證據與命中原因位於 `website-page-classification.json`。",
        "",
        "`pages/98-非頁面-共用功能.md` 與 `pages/99-待人工確認頁面.md` 另由 `scripts/enrich-msg-cross-cutting-requirements.py` 依 MSG project-docs 業務流程補上跨頁參考；這些參考不會取代選單分類，也不會把待確認需求強制歸入頁面。",
    ]
    (OUT / "page-classification-index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    source_data = json.loads(SOURCE.read_text(encoding="utf-8"))
    menu = json.loads(MENU.read_text(encoding="utf-8"))
    menu_pages = flatten_menu(menu)
    menu_keys = {(page["name"], page["url"]): page for page in menu_pages}
    groups = OrderedDict((key, []) for key in menu_keys)
    groups[("非頁面／共用功能", "")] = []
    groups[("待人工確認頁面", "")] = []
    evidence = {}

    for issue in source_data["issues"]:
        page, url, reason, pattern = classify(issue)
        key = (page, url)
        groups.setdefault(key, []).append(issue)
        evidence[str(issue["id"])] = {
            "page": page,
            "url": url,
            "reason": reason,
            "matched_rule": pattern,
        }

    PAGES_OUT.mkdir(parents=True, exist_ok=True)
    for (page, url), issues in groups.items():
        lines = [
            f"# {page}",
            "",
            f"共 {len(issues)} 筆需求單。",
        ]
        menu_page = menu_keys.get((page, url))
        if menu_page:
            lines += [
                f"目錄：{menu_page['group_name']}",
                f"目錄排序：`{menu_page['group_order']}`（sort={menu_page['group_sort']}）",
                f"頁面排序：`{menu_page['page_order']}`（sort={menu_page['sort']}）",
                f"網站路由：`{url}`",
                f"accessLevel：`{menu_page['accessLevel']}`",
            ]
        elif page == "非頁面／共用功能":
            lines.append("此分類保留沒有單一 MSG 選單頁面的 API、JOB、Webhook、聊天室、LINE 綁定與共用技術需求。")
        else:
            lines.append("此分類保留目前無法可靠對應到 MSG 選單頁面的需求，需人工確認。")
        lines += [
            "",
            "> 依 MSG 實際選單分類；需求單標題優先，描述補充。完整命中證據見 `../website-page-classification.json`。",
            "",
            "| 需求單 | 專案 | 標題 | 類型 | 狀態 | 負責人 | 建立日期 | 命中位置 |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for issue in sorted(issues, key=lambda item: item["id"], reverse=True):
            lines.append(issue_row(issue, evidence[str(issue["id"])]))
        (PAGES_OUT / file_name(page, menu_page)).write_text("\n".join(lines) + "\n", encoding="utf-8")

    classification = {
        "source": str(SOURCE.relative_to(ROOT)),
        "menu": str(MENU.relative_to(ROOT)),
        "total": len(source_data["issues"]),
        "menu_pages": len(menu_pages),
        "categories": {f"{page}|{url}": len(issues) for (page, url), issues in groups.items()},
        "evidence": evidence,
    }
    (OUT / "website-page-classification.json").write_text(
        json.dumps(classification, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_page_purpose_index(menu_pages, load_l2_index())
    write_classification_index(menu_pages, groups, evidence, source_data)
    pending_count = len(groups[("待人工確認頁面", "")])
    print(
        f"完成：{len(source_data['issues'])} 筆需求單、{len(menu_pages)} 個 MSG 選單頁面、"
        f"{len(groups)} 個分類；待人工確認 {pending_count} 筆"
    )


if __name__ == "__main__":
    main()
