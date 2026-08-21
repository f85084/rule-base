#!/usr/bin/env python3
"""依 MSG project-docs 業務流程補充 98/99 需求單的流程對照。"""

import json
import re
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ISSUES_SOURCE = ROOT / "data/sources/msg/redmine/issues_all.json"
CLASSIFICATION_SOURCE = ROOT / "docs/msg/requirements/website-page-classification.json"
OUTPUT_DIR = ROOT / "docs/msg/requirements/pages"
PROJECT_DOCS_ROOT = Path("/home/art/openab-repos/project-docs/projects/MSG")
BUSINESS_FLOW_ROOT = PROJECT_DOCS_ROOT / "data/business-flows"
BASE_URL = "https://redmine.etzone.net/issues"


# 這些是「跨頁／共用流程」的業務對照，不會改變既有的網站選單分類。
# 規則順序代表優先權；標題與描述合併比對，避免只看技術關鍵字而失去業務脈絡。
FLOW_SPECS = OrderedDict(
    [
        (
            "webhook",
            {
                "name": "LINE Webhook 與客戶生命週期",
                "description": "涵蓋 follow、unfollow、message、postback 等事件，以及 profile、client、client_user、chatroom 與訊息保存的生命週期。",
                "patterns": [
                    r"webhook|web hook|follow|unfollow|postback|redelivery|Line\s*SDK|LINE\s*Profile|LINE\s*Channel|好友首次",
                ],
                "sources": [
                    "data/business-flows/special/MSG-LINE-Webhook客戶生命週期.md",
                    "data/business-flows/WebAPI/L1/WebHook.md",
                    "data/business-flows/WebAPI/log-map/WebHook.md",
                ],
            },
        ),
        (
            "binding",
            {
                "name": "LINE／LIFF 身分綁定與客戶身分",
                "description": "涵蓋 LIFF 登入、手機／客代綁定、OTP、客戶身分驗證及綁定後的客戶資料同步。",
                "patterns": [
                    r"LIFF|Liff|liff|綁定|客代|手機驗證|電話驗證|驗證碼|OTP|好友綁定|手機號碼",
                ],
                "sources": [
                    "data/business-flows/special/MSG-LIFF手機驗證與客代綁定.md",
                    "data/business-flows/special/MSG-B2C-LIFF身分驗證.md",
                    "data/business-flows/B2E/L1/Customer.md",
                ],
            },
        ),
        (
            "chat",
            {
                "name": "B2E 即時客服對話、訊息與派線",
                "description": "涵蓋聊天室、訊息保存、SignalR 即時通知、客戶狀態、未讀數、離線留言與客服派線。",
                "patterns": [
                    r"聊天室|聊天|對話|訊息|留言|離線|SignalR|ChatHub|派線|指派|轉接|未讀|封鎖|解封鎖|線上人數|lastSeq|chatroom",
                ],
                "sources": [
                    "data/business-flows/B2E/L3/即時客服對話與派線流程.md",
                    "data/business-flows/special/MSG-訊息保存即時通知與離線回覆.md",
                    "data/business-flows/B2E/L1/Chatroom.md",
                    "data/business-flows/B2E/L1/Message.md",
                    "data/business-flows/B2E/L1/Assign.md",
                ],
            },
        ),
        (
            "marketing",
            {
                "name": "B2E 行銷群發與內容素材",
                "description": "涵蓋群發、模板、商品、圖庫、圖文選單與素材在多個管理頁面間的串接。",
                "patterns": [
                    r"群發|群組訊息|模板|商品|圖庫|圖片庫|圖文選單|Richmenu|推播|推薦商品|上傳順序|素材|文案|關鍵字",
                ],
                "sources": [
                    "data/business-flows/B2E/L3/行銷群發與內容素材管理.md",
                    "data/business-flows/B2E/L1/Multi.md",
                    "data/business-flows/B2E/L1/Combo.md",
                    "data/business-flows/B2E/L1/Gallery.md",
                    "data/business-flows/B2E/L1/Product.md",
                ],
            },
        ),
        (
            "audience",
            {
                "name": "B2E 受眾、客戶與標籤",
                "description": "涵蓋客戶名單、會員資料、受眾分群、標籤、客戶狀態與資料同步等跨頁資料流。",
                "patterns": [
                    r"受眾|分眾|標籤|客戶名單|客戶資料|客戶狀態|會員|好友|客戶等級|電話隱碼",
                ],
                "sources": [
                    "data/business-flows/B2E/L3/受眾分群與標籤管理.md",
                    "data/business-flows/B2E/L1/Audience.md",
                    "data/business-flows/B2E/L1/Customer.md",
                    "data/business-flows/B2E/L1/CustomerCheck.md",
                    "data/business-flows/B2E/L1/Tag.md",
                ],
            },
        ),
        (
            "activity",
            {
                "name": "B2E 互動行銷、簽到與遊戲",
                "description": "涵蓋活動管理、照片合成、遊戲、簽到與 B2C 活動頁之間的互動流程。",
                "patterns": [
                    r"簽到|報到|印章|遊戲|抽獎|刮刮卡|搖搖樂|活動|照片合成|合成圖片|同框照|活動頁|拍照|報名名單|成果儀表版",
                ],
                "sources": [
                    "data/business-flows/B2E/L3/互動行銷與簽到遊戲管理.md",
                    "data/business-flows/B2E/L1/CheckIn.md",
                    "data/business-flows/B2E/L1/GameManage.md",
                    "data/business-flows/B2E/L1/FrameMergeActivity.md",
                    "data/business-flows/B2C/L1/CheckIn.md",
                ],
            },
        ),
        (
            "observability",
            {
                "name": "B2E 直播、統計與 AI",
                "description": "涵蓋直播、對話／訊息統計、AI 助手、摘要與 AI 費用等觀測和分析流程。",
                "patterns": [
                    r"直播|見面會|統計|報表|AI|人工智慧|摘要|費用|成本|Metrics|ELK|GTM|GA|Google\s*Analytics",
                ],
                "sources": [
                    "data/business-flows/B2E/L3/直播、統計與費用監控.md",
                    "data/business-flows/B2E/L1/Stream.md",
                    "data/business-flows/B2E/L1/Metrics.md",
                    "data/business-flows/B2E/L1/MessagesMetrics.md",
                    "data/business-flows/B2E/L1/ChatAI.md",
                ],
            },
        ),
        (
            "identity",
            {
                "name": "B2E 登入、帳號與權限",
                "description": "涵蓋本機登入、MI SSO、自動建帳、使用者／角色／功能權限及帳號狀態。",
                "patterns": [
                    r"登入|登出|帳號|帳戶|使用者|角色|權限|SSO|MI|LDAP|AD|Token|JWT|Session|session|專員帳號|維運專員|新建使用者",
                ],
                "sources": [
                    "data/business-flows/B2E/L3/登入與安全權限治理.md",
                    "data/business-flows/special/MSG-MI-SSO自動建立帳號機制.md",
                    "data/business-flows/special/MSG-V_OBLINE與自動建帳耦合背景.md",
                    "data/business-flows/B2E/L1/SSO.md",
                    "data/business-flows/B2E/L1/User.md",
                    "data/business-flows/B2E/L1/Role.md",
                ],
            },
        ),
        (
            "shared",
            {
                "name": "共用技術、資料與維運",
                "description": "涵蓋沒有單一前台頁面、也無法安全歸入特定業務流程的架構、資料、排程、環境與共用元件。",
                "patterns": [],
                "sources": [
                    "data/business-flows/INDEX.md",
                    "data/business-flows/B2E/L1/INDEX.md",
                    "data/business-flows/special/MSG-前後端版本切換自動重整.md",
                    "data/business-flows/special/MSG-訊息保存即時通知與離線回覆.md",
                ],
            },
        ),
    ]
)


def escape_cell(value):
    return str(value or "").replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def issue_link(issue_id):
    return f"[{issue_id}]({BASE_URL}/{issue_id})"


def source_link(relative_path):
    absolute = PROJECT_DOCS_ROOT / relative_path
    label = Path(relative_path).name
    # 產出文件位於 docs/msg/requirements/pages/，往上五層才回到 openab-repos。
    href = f"../../../../../project-docs/projects/MSG/{relative_path}"
    if absolute.exists():
        return f"[{escape_cell(label)}]({href})"
    return f"`{relative_path}`（尚未找到檔案）"


def source_list(paths, limit=None):
    selected = paths[:limit] if limit else paths
    return "、".join(source_link(path) for path in selected)


def classify_flow(issue):
    subject = issue.get("subject", "")
    description = issue.get("description", "")
    if re.search(r"Host\s*log|個資遮罩|個資遮蔽|MaskInLog", subject, re.IGNORECASE):
        return "shared"
    # 先看標題，讓「聊天室傳送圖片」不會因描述提到綁定而被移到身分流程；
    # 只有標題沒有候選時才用描述補充，維持與網站選單分類器相同的可解釋順序。
    for key, spec in FLOW_SPECS.items():
        if any(re.search(pattern, subject, re.IGNORECASE) for pattern in spec["patterns"]):
            return key
    for key, spec in FLOW_SPECS.items():
        if any(re.search(pattern, description, re.IGNORECASE) for pattern in spec["patterns"]):
            return key
    return "shared"


def load_data():
    issues = json.loads(ISSUES_SOURCE.read_text(encoding="utf-8"))["issues"]
    classification = json.loads(CLASSIFICATION_SOURCE.read_text(encoding="utf-8"))
    evidence = classification["evidence"]
    selected = []
    for issue in issues:
        item = evidence.get(str(issue["id"]))
        if item and item["page"] in {"非頁面／共用功能", "待人工確認頁面"}:
            selected.append((issue, item))
    return selected


def issue_columns(issue, evidence):
    return {
        "id": issue_link(issue["id"]),
        "project": escape_cell(issue.get("project", {}).get("name", "")),
        "subject": escape_cell(issue.get("subject", "")),
        "tracker": escape_cell(issue.get("tracker", {}).get("name", "")),
        "status": escape_cell(issue.get("status", {}).get("name", "")),
        "assigned": escape_cell(issue.get("assigned_to", {}).get("name", "未指派")),
        "created": escape_cell(issue.get("created_on", "")[:10]),
        "evidence": escape_cell(evidence.get("reason", "")),
    }


def render_issue_table(items, extra_header="業務流程對照", extra_value=None):
    lines = [
        f"| 需求單 | 專案 | 標題 | 類型 | 狀態 | 負責人 | 建立日期 | 命中位置 | {extra_header} |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for issue, evidence in items:
        row = issue_columns(issue, evidence)
        value = extra_value(issue, evidence) if extra_value else ""
        lines.append(
            f"| {row['id']} | {row['project']} | {row['subject']} | {row['tracker']} | "
            f"{row['status']} | {row['assigned']} | {row['created']} | {row['evidence']} | {value} |"
        )
    return lines


def write_shared(items):
    grouped = OrderedDict((key, []) for key in FLOW_SPECS)
    for issue, evidence in items:
        grouped[classify_flow(issue)].append((issue, evidence))

    lines = [
        "# 非頁面／共用功能",
        "",
        f"共 {len(items)} 筆需求單。",
        "此分類保留沒有單一 MSG 選單頁面的 API、JOB、Webhook、聊天室、LINE 綁定與共用技術需求。",
        "",
        "> 依 MSG 實際選單分類；需求單先依標題、再以描述補充。以下再依 MSG project-docs 的業務流程整理跨頁脈絡。",
        "> 這些業務流程是閱讀與追溯用的參考，不代表需求單已完成、已驗證或一定屬於該流程；實際程式與環境行為優先。",
        "",
        "## 業務流程分布",
        "",
        "| 業務流程 | 需求單數 | 主要參考來源 |",
        "|---|---:|---|",
    ]
    for key, spec in FLOW_SPECS.items():
        if not grouped[key]:
            continue
        lines.append(f"| {spec['name']} | {len(grouped[key])} | {source_list(spec['sources'], 2)} |")

    for index, (key, spec) in enumerate(FLOW_SPECS.items(), 1):
        if not grouped[key]:
            continue
        lines += [
            "",
            f"## {index}. {spec['name']}",
            "",
            spec["description"],
            "",
            f"參考業務流程與技術文件：{source_list(spec['sources'])}",
            "",
        ]
        lines.extend(render_issue_table(grouped[key], "分類說明", lambda issue, evidence: f"{spec['name']}；{evidence.get('reason', '')}"))

    lines += [
        "",
        "## 分類規則",
        "",
        "本文件只整理已被選單分類器判定為「非頁面／共用功能」的需求單；不會把它們改成任何 MSG 選單頁面。業務流程分組由 `scripts/enrich-msg-cross-cutting-requirements.py` 依標題與描述關鍵字產生，完整選單分類證據仍以 `../website-page-classification.json` 為準。",
    ]
    (OUTPUT_DIR / "98-非頁面-共用功能.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return grouped


def pending_reason(issue, evidence, flow_key):
    spec = FLOW_SPECS[flow_key]
    if flow_key == "shared":
        return "未命中選單分類規則，且目前標題／描述不足以建立可靠的業務流程候選。"
    return f"未命中選單分類規則；僅能依標題／描述提出候選流程「{spec['name']}」，仍需人工確認實際頁面或模組。"


def write_pending(items):
    grouped = OrderedDict((key, []) for key in FLOW_SPECS)
    for issue, evidence in items:
        grouped[classify_flow(issue)].append((issue, evidence))

    lines = [
        "# 待人工確認頁面",
        "",
        f"共 {len(items)} 筆需求單。",
        "此分類保留目前無法可靠對應到 MSG 選單頁面的需求，需人工確認，不自動歸入任何選單頁。",
        "",
        "> 依 MSG 實際選單分類；需求單先依標題、再以描述補充。以下只提供業務流程候選與參考來源，候選不是正式分類。",
        "> 完整命中證據見 `../website-page-classification.json`；實際程式與環境行為優先。",
        "",
        "## 候選流程分布",
        "",
        "| 候選業務流程 | 需求單數 | 判斷 |",
        "|---|---:|---|",
    ]
    for key, spec in FLOW_SPECS.items():
        if grouped[key]:
            judgement = "可作為人工確認起點" if key != "shared" else "尚無可靠候選，需補充上下文"
            lines.append(f"| {spec['name']} | {len(grouped[key])} | {judgement} |")

    lines += [
        "",
        "## 待確認需求明細",
        "",
        "| 需求單 | 專案 | 標題 | 類型 | 狀態 | 負責人 | 建立日期 | 未分類原因 | 候選業務流程／參考來源 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for key, spec in grouped.items():
        for issue, evidence in spec:
            flow_spec = FLOW_SPECS[key]
            row = issue_columns(issue, evidence)
            reason = escape_cell(pending_reason(issue, evidence, key))
            if key == "shared":
                candidate = "尚無可靠候選；" + source_list(flow_spec["sources"], 2)
            else:
                candidate = f"候選：{flow_spec['name']}；" + source_list(flow_spec["sources"], 3)
            lines.append(
                f"| {row['id']} | {row['project']} | {row['subject']} | {row['tracker']} | "
                f"{row['status']} | {row['assigned']} | {row['created']} | {reason} | {candidate} |"
            )

    lines += [
        "",
        "## 人工確認方式",
        "",
        "1. 先從需求描述、畫面截圖、驗收條件或相關程式確認實際頁面／模組。",
        "2. 若確認屬於 MSG 選單頁面，調整 `scripts/classify-msg-by-website-menu.py` 的規則後重新產生分類文件。",
        "3. 若仍是 API、JOB、Webhook 或跨頁共用功能，保留在 98，並視需要調整本文件的業務流程候選。",
    ]
    (OUTPUT_DIR / "99-待人工確認頁面.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return grouped


def main():
    selected = load_data()
    shared = [(issue, evidence) for issue, evidence in selected if evidence["page"] == "非頁面／共用功能"]
    pending = [(issue, evidence) for issue, evidence in selected if evidence["page"] == "待人工確認頁面"]
    write_shared(shared)
    write_pending(pending)

    expected = len(shared) + len(pending)
    if expected != 211:
        raise SystemExit(f"預期 98/99 合計 211 筆，實際為 {expected} 筆；請先確認分類快照。")
    print(f"已更新 98 非頁面／共用功能：{len(shared)} 筆")
    print(f"已更新 99 待人工確認頁面：{len(pending)} 筆")
    print(f"業務流程參考根目錄：{BUSINESS_FLOW_ROOT}")


if __name__ == "__main__":
    main()
