# MSG／CSP 一般人員操作手冊化交付報告

## 實際修改檔案

本次 writer 依 brief 修改下列授權文件；既有其他 dirty／untracked 工作未清理、未 reset、未 checkout：

- `docs/msg/operations/一般人員操作手冊.md`
- `docs/msg/operations/01-登入與帳號.md`
- `docs/msg/operations/02-聊天室與客服.md`
- `docs/msg/operations/03-派線與離線訊息.md`
- `docs/msg/operations/04-客戶查詢.md`
- `docs/msg/operations/05-受眾與標籤.md`
- `docs/msg/operations/06-訊息素材與群發.md`
- `docs/msg/operations/07-活動與簽到.md`
- `docs/msg/operations/08-查詢統計與直播.md`
- `docs/csp/operations/日常作業.md`
- `docs/csp/operations/客戶服務.md`
- `docs/csp/operations/接單與訂單.md`
- `docs/csp/operations/訊息查詢與通知中心.md`
- `docs/csp/operations/軟體電話.md`
- `docs/csp/operations/商品與特殊接單.md`
- `docs/csp/operations/LINE綁定與AI助手.md`
- `docs/csp/operations/04-TM名單推薦.md`
- `docs/csp/operations/05-客戶查詢.md`
- `docs/csp/operations/06-接單作業.md`
- `docs/csp/operations/07-訂單管理.md`
- `docs/csp/operations/09-客訴處理.md`
- `docs/csp/operations/12-聯繫歷史.md`
- `docs/csp/operations/13-電話小結作業.md`
- `docs/csp/operations/14-客服員待辦事項.md`
- `docs/csp/operations/17-票劵-預約.md`
- `docs/csp/operations/18-直播-見面會報名.md`
- `docs/csp/operations/19-商品訊息.md`
- `docs/csp/operations/20-訊息查詢.md`
- `docs/csp/operations/21-通知中心.md`
- `docs/csp/operations/22-調聽音檔.md`
- `docs/csp/operations/24-訂單質檢.md`
- `docs/csp/operations/26-質檢查詢.md`
- `docs/csp/operations/28-客戶進階查詢.md`
- `docs/csp/operations/29-客服即時狀態.md`
- `docs/csp/operations/30-客服文件管理.md`
- `docs/csp/operations/37-直播-見面會管理.md`
- `docs/csp/operations/38-行事曆.md`
- `docs/csp/operations/47-小結清單.md`
- `.coordination/tasks/manualize-msg-csp-operations-20260821/report.md`

## 內容證據與實作

- 先閱讀 `/home/art/AGENTS.md`、`/home/anna/AGENTS.md`、`docs/csp/operations/AGENTS.md`、本 task `brief.md`，並盤點既有 MSG／CSP 操作文件、`docs/msg/README.md`、`docs/csp/README.md` 與 MSG B2E L1/L2/L3 business-flow 索引及相關文件。
- MSG 一般人員索引改為先依工作目的選頁，再依單頁的入口、角色、權限／前置、畫面步驟、完成判斷與第一個排錯操作；技術、需求與 business-flow 來源留在後段。
- MSG 01–08 各頁補上一般人員可照做的入口與角色界線、開始前條件、按頁面／欄位／分頁判讀的步驟、每步預期結果、完成確認、影響／限制與第一個排錯；各頁原有 route 子流程與來源內容保留作技術補充。
- `06-訊息素材與群發.md` 保留 `/Richmenu` 與 `RichmenuSlave` 的來源邊界，並以 [05-受眾與標籤](../../../docs/msg/operations/05-受眾與標籤.md) 及 Audience L2 交叉導覽群發受眾前置。
- CSP 授權清單的 29 份操作文件各補一般人員入口區塊，將正常操作置於技術查核內容之前；未新增截圖，也未把需求狀態或來源描述寫成已部署保證。
- 無法由本地來源確認的按鈕、欄位、資料同步、外部送達、現行權限與部署版本，均保留為 `runtime unknown` 或待以當期 UI／管理者確認；`current`、`historical`、`inference` 分開標示。

## Checks

- `git diff --check`：通過。
- MSG 索引與 01–08 結構檢查：通過；每頁有標題、入口／角色、開始前／權限、編號步驟、預期結果／完成判斷、常見問題／第一個排錯及需求／business-flow 或技術補充段落。
- CSP 授權文件結構檢查：通過；各頁已保留原有技術內容並有一般人員入口、操作步驟、預期結果、完成判斷、排錯與來源／技術補充。
- 本地 Markdown 連結／目標檔案檢查：通過；檢查 `docs/msg/operations`、`docs/csp/operations` 與本 task 文件，共 81 份 Markdown、757 個本地連結，缺失 0。
- 唯一完成標記檢查：通過；本檔只有一個 `FINAL: COMPLETE`，且位於最後一行。

## 限制與未執行的外部操作

- 沒有執行 Herdr、source、Panel 派工、登入、runtime／部署驗證、外部服務查詢、commit、push、deploy、restart 或其他外部操作。
- 沒有修改來源資料、需求快照、程式碼、review.md 或 brief 以外的授權範圍；未驗證實際環境中的 UI 文字、角色權限、資料同步、LINE 送達率、報表正確性與目前部署狀態。
- 本報告與文件內容是本地來源整理與操作指引，不構成需求已完成或功能已部署的保證。

FINAL: COMPLETE
