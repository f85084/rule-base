# Task brief: MSG 一般人員手冊 CSP 化與 Herdr 頁籤拓撲修正

## 目標

將 MSG 一般人員操作手冊改成 `/home/art/openab-repos/rule-base/docs/csp/operations/` 採用的操作文件風格，並把 `/home/anna/AGENTS.md` 的 11n 實體視窗規則修正為「主協調頁與 worker 頁分離、worker 角色與 portable 1:1:N 流程一致」。

## 角色與交接

- Coordinator：目前主協調者，負責 bounded scope、派工、驗收與最終回報。
- 唯一 writer：一名可見、互動式 Herdr `codex` worker，在唯一 `WORKERS` 頁籤執行本 brief 的文件與規則修改，完成後寫入本 task 的 `report.md`。
- 唯一 reviewer：writer 完成後，在同一 `WORKERS` 頁籤使用另一個可見、互動式 Herdr `codex` panel 唯讀審查，完成後寫入本 task 的 `review.md`，不得修改 writer 產出。
- 交接：writer／reviewer 以 report／review 與一次完成通知交回 coordinator；coordinator 再核對 workspace、diff、連結、檢查與既有 dirty work。

## 授權修改範圍

### 工作規則

- `/home/anna/AGENTS.md`
  - 只修正 Herdr topology、11n routing 與範例中的矛盾描述。
  - 明確定義：目前頁籤是 coordinator 主頁；唯一共享 `WORKERS` 頁籤是 11n writer/reviewer 的可見工作頁；`WORKERS` 最多四個 panel，重用 idle panel，並固定為可辨識的 2×2 worker 區；不得把 worker panel 塞回 coordinator 主頁。
  - 保留 portable 1:1:N 的 coordinator／writer／reviewer／report／review／acceptance 閘門。
  - 非 11n 的長任務仍使用與共享 `WORKERS` 分開的 `WORKERS-<TASK_ID>` 頁籤；同一 task 的 writer、reviewer 與命令留在該頁籤。
  - 不修改 Git 身分、摘要規則、權限提示或其他與本問題無關的規則。

### MSG 文件

- `docs/msg/operations/一般人員操作手冊.md`
  - 改為短索引／入口頁，只保留一般人員如何選擇工作文件、資料界線、共通安全提醒與來源導覽。
  - 不再把八個領域的完整步驟全部塞在同一檔案。
- 新增下列 8 份 CSP 風格操作文件，每份以「一個工作頁／工作流程」為主，服務一般使用人員；內容至少包含：敘述狀態與查核界線、適用人員與入口、正常操作、完成判斷、權限／前置條件、會造成的變更與限制、第一個檢查方向、需求單與 business-flow 來源。
  - `docs/msg/operations/01-登入與帳號.md`
  - `docs/msg/operations/02-聊天室與客服.md`
  - `docs/msg/operations/03-派線與離線訊息.md`
  - `docs/msg/operations/04-客戶查詢.md`
  - `docs/msg/operations/05-受眾與標籤.md`
  - `docs/msg/operations/06-訊息素材與群發.md`
  - `docs/msg/operations/07-活動與簽到.md`
  - `docs/msg/operations/08-查詢統計與直播.md`
- `docs/msg/README.md` 僅在需要時補上上述入口連結；不得改動其他目錄的既有變更。
- `.coordination/tasks/msg-user-manual-csp-and-herdr-topology-20260821/report.md`

## 唯一事實來源

- CSP 樣式與內容邊界：`docs/csp/README.md`、`docs/csp/operations/24-訂單質檢.md`、`docs/csp/operations/04-TM名單推薦.md`。
- MSG 業務流程：`/home/art/openab-repos/project-docs/projects/MSG/data/business-flows/INDEX.md`、`B2E/L2/INDEX.md`、`B2E/L3/INDEX.md` 及其被索引的 MSG L2/L3 文件。
- MSG 需求對照：`docs/msg/requirements/README.md`、`docs/msg/requirements/pages/` 與既有 `data/sources/msg/redmine/` 快照。需求狀態不可當成 runtime 已部署證明。
- 視窗協作規則：`/home/art/portable-1-1-n-steering/README.md`、`/home/art/docs/agent/1-1-n/INDEX.md` 及其 `roles-and-gates.md`、`lifecycle-and-handoff.md`、`delivery-and-safety.md`。

## 排除範圍

- 不修改 `project-docs` 的來源文件、需求快照、測試資料、程式碼、部署、外部服務、Secret 或 runtime 設定。
- 不刪除、reset、checkout、覆寫或整理既有 dirty／untracked 變更。
- 不 commit、push、restart 或 deploy。
- 不補造未在來源確認的按鈕、角色、API、資料同步時效或成功送達保證；應標為 current／historical／inference／runtime unknown。

## 檢查與驗收

- `git diff --check`。
- 檢查新增索引連結存在，操作文件內的來源連結可解析；不得留下 `TODO` 或未完成佔位語句。
- 對照 CSP 範例，確認索引與操作文件分層，八份文件各自可被一般人員獨立閱讀。
- 對照 portable 1:1:N，確認 coordinator、唯一 11n `WORKERS`、非 11n `WORKERS-<TASK_ID>`、最多四 panel、報告／審查／驗收規則沒有互相矛盾。
- report 與 review 各只保留一個 final marker；reviewer 只寫 `review.md`，不修改 writer 產出。

## Stage 3 修正授權

reviewer 已提出 NEEDS REVISION；以下是本次唯一修復切片，仍由原 writer 在既有 `WORKERS` writer Panel 執行，完成後更新同一份 `report.md`，不得另開 task 或把修復交給 coordinator：

- 將 8 份操作文件補成可獨立閱讀的 CSP 風格領域入口：對文件內列出的每個 route／頁面加入獨立子流程，至少交代該頁的主要欄位／分頁判讀、資料來源或合併邊界、寫入／對外副作用、空資料／部分失敗判讀與 route-specific 第一個排錯；保留 current／historical／inference／runtime unknown 標示。
- `06-訊息素材與群發.md` 補上 `/Richmenu`／`RichmenuSlave` 的 L2 canonical source，並為跨到 `/Audience` 的前置補回 `05-受眾與標籤.md` 及 Audience L2／需求來源。
- `/home/anna/AGENTS.md` 將完成後 Panel 規則改成：完成 handoff 後可重用的 idle Panel 預設保留；只關閉無效／stale Panel，或由 coordinator 依容量與清理決策關閉，不能把所有 idle Panel 一律關閉。
- 更新 writer `report.md` 的內容證據與修正紀錄，但全檔仍只保留一個 `FINAL: COMPLETE`。

Stage 3 不得修改其他既有 dirty／untracked、來源、需求快照、程式碼或外部服務；完成後 reviewer 重新唯讀檢查並把同一 `review.md` 的唯一 final marker 改為 `FINAL: APPROVED` 或再次列出 NEEDS REVISION。

## 完成標記

writer：`FINAL: COMPLETE` 或 `FINAL: BLOCKED`，寫在 `report.md` 最後且只出現一次。

reviewer：`FINAL: APPROVED`、`FINAL: NEEDS REVISION` 或 `FINAL: BLOCKED`，寫在 `review.md` 最後且只出現一次。

coordinator 只有在 report、review、workspace diff 與檢查都通過後，才可將本 task 視為 accepted；本 brief 不授權任何 Git 發佈。
