#!/usr/bin/env python3
"""依網站實際選單頁面整理 Redmine 需求單。"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/sources/csp/redmine/issues_all.json"
MENU = ROOT / "data/sources/csp/website-menus.json"
OUT = ROOT / "docs/csp/requirements/pages"
BASE_URL = "https://redmine.etzone.net/issues"

# 以實際頁面名稱建立規則；規則順序代表優先權，標題優先於描述。
RULES = [
    ("系統功能", "/Function", r"系統功能|功能權限"),
    ("系統角色", "/Role", r"系統角色|角色管理|角色功能|角色權限|角色設定"),
    ("帳號設定", "/User", r"帳號設定|帳號管理|使用者帳號|AD帳號|帳號鎖定"),
    ("TM名單推薦", "/OutBoundTmList", r"TM名單|TM推薦|人物誌|人物摘要|360畫像|360標籤|標籤評價|點讚|推薦名單|客戶分群|分群推薦"),
    ("客戶查詢", "/CustomerService", r"客戶查詢|客服查詢|CustomerService"),
    ("接單作業", "/Order", r"接單作業|接單|訂購|下單|商品查詢"),
    ("銷退管理", "/Return", r"銷退|退貨|換貨|拒收|退回"),
    ("訂單管理", "/OrderHistory", r"訂單管理|訂單|配送|發票|載具|訂閱制|付款|信用卡|購物車|商品|分期|零卡|ATM匯款|購樂趣|結帳區|快速到貨|超取|宅家取|折價券|退款帳號"),
    ("客訴處理", "/CustomerComplaint", r"客訴|抱怨|CustomerComplaint"),
    ("會員明細", "/Customer", r"會員明細|會員資料|會員|客戶資料|大健康|切換客戶|切換指定客戶|新增地址|Customer(?!Service)|ContactId|手機資料"),
    ("帳戶明細", "/DiscountTransaction", r"帳戶明細|帳戶交易|現金帳戶|藍鑽|點數|E幣|貴賓券"),
    ("聯繫歷史", "/ContactHistory", r"聯繫歷史|聯絡記錄|交談記錄|互動記錄|訊息歷史"),
    ("電話小結作業", "/CallSummary", r"電話小結|通話小結|小結作業|小結內容|小結欄位"),
    ("客服員待辦事項", "/OutBoundTodoList", r"客服員待辦|待辦事項|客服待辦"),
    ("問卷管理", "/Survey", r"問卷|問券|Survey|第一題"),
    ("活動管理", "/Activity", r"活動管理|活動設定|東森樂透|小額奪寶|活動報名|限量品|樂透|行銷活動"),
    ("票劵/預約", "/NaturalBeauty", r"票券|票劵|預約|自然美"),
    ("直播/見面會報名", "/LiveStreamSignUp", r"直播報名|見面會報名|直播/見面會報名|報名介面|報名明細|歷史報名"),
    ("商品訊息", "/SaleMessage", r"商品訊息|商品話術|銷售話術"),
    ("訊息查詢", "/Message", r"訊息查詢|傳送訊息|訊息紀錄|即時訊息|歷史訊息|發送訊息|訊息轉發|簡訊|Message|LINE"),
    ("通知中心", "/Notifications", r"通知中心|通知|提醒|推播"),
    ("調聽音檔", "/AudioLog", r"調聽音檔|音檔管理|調聽撥放|調聽播放器|音檔播放器|音檔位置|錄音|播放清單|撥放清單|connection.?id|ConnId|SIP.?Record"),
    ("優質音檔", "/AudioShared", r"優質音檔|優良音檔|分享音檔|話術音檔"),
    ("訂單質檢", "/OrderQA", r"訂單質檢|質檢單|質檢流程|質檢批次|質檢類型|質檢匯入|質檢Excel|質檢累犯|質檢歷程|質檢主檔|查核質檢|組長質檢|質檢的音檔|新增質檢|獎勵質檢|大批質檢|自首件|OrderQA"),
    ("質檢查核", "/OrderQACheck", r"質檢查核|質檢審核|複審|OrderQACheck"),
    ("質檢查詢", "/OrderQAQuery", r"質檢查詢|質檢報表|質檢匯出|OrderQAQuery"),
    ("質檢項目維護", "/OrderQAStandard", r"質檢項目|質檢標準|OrderQAStandard"),
    ("客戶進階查詢", "/SuperiorQuery", r"客戶進階查詢|進階查詢|SuperiorQuery"),
    ("客服即時狀態", "/OutBoundStatus", r"客服即時狀態|即時客服狀態|線上狀態"),
    ("客服文件管理", "/Document", r"客服文件|文件管理|讀取文件|下載文件|Document(?!QA)"),
    ("使用者設定", "/Agent", r"代理人設定|職務代理人|代理清單|代理人|使用者設定"),
    ("審核作業", "/Review", r"審核作業|審核功能|審核清單|待審資料|Review"),
    ("跑馬燈管理", "/Marquee", r"跑馬燈"),
    ("公告管理", "/Announcement", r"公告管理|公告"),
    ("組織部門設定", "/Department", r"部門|組織|組織階層"),
    ("直播/見面會管理", "/LiveStreamManage", r"直播/見面會管理|直播管理|見面會管理|直播/見面會活動類型"),
    ("行事曆管理", "/Meeting", r"行事曆管理|管理行事曆|工作日|Meeting"),
    ("行事曆", "/Calendar", r"行事曆|課程|記事本"),
    ("商品加量管理", "/ProductIncrease", r"商品加量|加量管理"),
    ("外呼組別管理", "/OutBoundTeam", r"外呼組別|組別成員"),
    ("名單歷程查詢", "/OutBoundCustomer", r"名單歷程|名單查詢|名單記錄|名單轉換"),
    ("名單轉派申請", "/OutBoundListTransferApply", r"轉派申請|申請轉派"),
    ("名單轉派審核", "/OutBoundListTransferReview", r"轉派審核|審核轉派"),
    ("名單轉派查詢", "/OutBoundListTransfer", r"名單轉派|轉派功能|轉派查詢|轉派歷程|轉派退件"),
    ("名單小組管理", "/OutBoundListManagement", r"名單小組|沉澱會員|名單回收"),
    ("小結清單", "/ContactSummary", r"小結清單|小結狀態|小結查詢"),
    ("撥號日期管理", "/DialScheduler", r"撥號日期|前置碼|DialScheduler"),
    ("Domain管理", "/DomainData", r"Domain管理|DomainData"),
    ("排程工作狀態", "/JobStatus", r"排程工作|JOB狀態|JobStatus"),
    ("工作日管理", "/WorkingDay", r"工作日管理|政府機關行事曆"),
    ("外部服務呼叫紀錄", "/ApiLog", r"外部服務|API Log|ApiLog|呼叫紀錄"),
    ("AI Prompt 管理", "/PromptManagement", r"Prompt設定|Prompt管理|提示詞設定"),
    ("AI 費用報表", "/AiCostReport", r"AI費用|AI 成本|費用報表"),
    ("小m文件管理", "/DocumentQA", r"小M文件|小m文件|文件給 AI|Qdrant"),
    ("小m使用紀錄", "/DocumentQARecord", r"小M使用|小m使用|問答紀錄|AI使用紀錄"),
    ("郵件通知紀錄", "/MailNotice", r"郵件通知|MailNotice|Mail"),
    ("非頁面／共用功能", "", r"軟體電話|CTI|SIP|API|JOB|排程|Redis|資料庫|DB|SP|SQL|sonarqube|原碼|架構|效能|快取|SSO|微服務|登入|login|登出|Session|Token|AntiForgery|HttpClient|traceId|全站|首頁|前端|ESM|Layout|header|Cache-Control|cache|webpack|Bundle|bundle|css|scss|sass|Style|樣式|字體|font|選單|左側|LightboxModal|500畫面|Log|LOG|爬蟲|MCP|Framework|framework|升版|Exception|exception|錯誤|環境|int溢位|儀表板|MI Search|圖檔存取|圖片剪裁|上傳圖片|我的最愛|modalHelper|字串轉換|暗系列|暗色系|AgentID|時間格式|AI|小M|小m|對話紀錄|問答|Tag|streaming|POC|驗證|功能優化|TempData|ajax|網頁|移除不必要|移除.*程式|地址元件|使用者物件|個人存放區|提示訊息|撈取專員使用|外撥|進線|通話中|頁面"),
]


def classify(issue):
    subject = issue.get("subject", "")
    body = subject + " " + issue.get("description", "")
    for page, url, pattern in RULES:
        if re.search(pattern, subject, re.IGNORECASE):
            return page, url, "標題"
    for page, url, pattern in RULES:
        if re.search(pattern, body, re.IGNORECASE):
            return page, url, "內容"
    return "待人工確認頁面", "", "未命中規則"


def esc(value):
    return str(value or "").replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def row(issue):
    link = f"[{issue['id']}]({BASE_URL}/{issue['id']})"
    return "| {} | {} | {} | {} | {} | {} |".format(
        link, esc(issue.get("subject")), esc(issue.get("tracker", {}).get("name")),
        esc(issue.get("status", {}).get("name")), esc(issue.get("assigned_to", {}).get("name", "未指派")),
        issue.get("created_on", "")[:10])


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    menu = json.loads(MENU.read_text(encoding="utf-8"))
    groups = {}
    evidence = {}
    for issue in data["issues"]:
        page, url, reason = classify(issue)
        groups.setdefault((page, url), []).append(issue)
        evidence[str(issue["id"])] = {"page": page, "url": url, "reason": reason}

    # 保留網站選單中目前沒有對應需求單的頁面，讓索引完整對齊網站。
    for group in menu["groups"]:
        for page in group["pages"]:
            groups.setdefault((page["name"], page["url"]), [])

    OUT.mkdir(parents=True, exist_ok=True)
    # 分類規則調整後，移除上一輪生成但本輪已不存在的頁面文件，避免殘留內容造成重複。
    for old_file in OUT.glob("*.md"):
        old_file.unlink()
    for (page, url), issues in sorted(groups.items(), key=lambda x: (-len(x[1]), x[0][0])):
        lines = [f"# {page}", "", f"共 {len(issues)} 筆需求單。"]
        if url:
            lines.append(f"網站路由：`{url}`")
        lines += ["", "> 依網站選單頁面分類；分類依需求單標題優先、描述補充。", "", "| 需求單 | 標題 | 類型 | 狀態 | 負責人 | 建立日期 |", "|---|---|---|---|---|---|"]
        lines.extend(row(issue) for issue in sorted(issues, key=lambda x: x["id"], reverse=True))
        if page == "待人工確認頁面":
            lines += ["", "## 待人工確認", "", "尚未能從需求單文字判斷對應的網站頁面，需人工對照實際功能。"]
        (OUT / f"{page.replace('/', '-').replace('／', '-')}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = {"source": str(SOURCE.relative_to(ROOT)), "menu": str(MENU.relative_to(ROOT)), "total": len(data["issues"]), "categories": {page: len(items) for (page, _), items in groups.items()}, "evidence": evidence}
    (ROOT / "docs/csp/requirements/website-page-classification.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rule_index = [
        "# CSP 需求單頁面分類 Index", "",
        f"來源需求單：`{SOURCE.relative_to(ROOT)}`",
        f"網站選單：`{MENU.relative_to(ROOT)}`", "",
        "## 分類流程", "",
        "1. 先讀取需求單標題，依下方規則的優先順序判斷。",
        "2. 標題沒有命中時，再用標題加需求描述全文判斷。",
        "3. 同一張需求單只歸入第一個命中的主要頁面。",
        "4. 沒有命中時才會進入「待人工確認頁面」；API、背景作業、共用元件與全站功能歸入「非頁面／共用功能」。",
        "5. 規則順序由具體頁面到共用功能；後面的規則不會覆蓋前面已命中的頁面。", "",
        "## 分類規則（依優先順序）", "",
        "| 順序 | 頁面 | URL | 判斷關鍵字／模式 |", "|---:|---|---|---|",
    ]
    for number, (page, url, pattern) in enumerate(RULES, 1):
        rule_index.append(f"| {number} | {page} | `{url or '—'}` | `{pattern.replace('|', ' · ')}` |")
    rule_index += [
        "", "## 分類結果", "",
        f"- 需求單總數：{len(data['issues'])}",
        f"- 分類總數：{len(groups)}（含網站頁面、非頁面／共用功能與待人工確認）",
        f"- 非頁面／共用功能：{len(groups.get(('非頁面／共用功能', ''), []))} 筆",
        f"- 待人工確認頁面：{len(groups.get(('待人工確認頁面', ''), []))} 筆",
        "- 每筆分類的實際命中依據另記錄於 `website-page-classification.json` 的 `evidence`。",
        "", "## 維護方式", "",
        "若網站新增或修改頁面，先更新 `data/sources/csp/website-menus.json`，再在本腳本的 `RULES` 補上頁面關鍵字，最後重新執行分類腳本。",
    ]
    (ROOT / "docs/csp/requirements/page-classification-index.md").write_text("\n".join(rule_index) + "\n", encoding="utf-8")
    print(f"完成：{len(data['issues'])} 筆，{len(groups)} 個網站頁面／非頁面分類")


if __name__ == "__main__":
    main()
