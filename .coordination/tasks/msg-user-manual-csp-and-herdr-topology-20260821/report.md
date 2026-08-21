# msg-user-manual-csp-and-herdr-topology-20260821 report

## 實際修改檔案

- `/home/anna/AGENTS.md`：補清 coordinator 主頁、共享唯一 `WORKERS` 頁、11n 固定 2×2／最多四個 Panel、以及非 11n `WORKERS-<TASK_ID>` 專用頁 routing；保留既有 1:1:N brief／report／review／acceptance 閘門。
- `docs/msg/operations/一般人員操作手冊.md`：改為短索引、共通安全提醒、選擇流程與來源導覽。
- `docs/msg/operations/01-登入與帳號.md`
- `docs/msg/operations/02-聊天室與客服.md`
- `docs/msg/operations/03-派線與離線訊息.md`
- `docs/msg/operations/04-客戶查詢.md`
- `docs/msg/operations/05-受眾與標籤.md`
- `docs/msg/operations/06-訊息素材與群發.md`
- `docs/msg/operations/07-活動與簽到.md`
- `docs/msg/operations/08-查詢統計與直播.md`
- `docs/msg/README.md`：補八份一般人員操作文件入口。
- 本報告：`.coordination/tasks/msg-user-manual-csp-and-herdr-topology-20260821/report.md`。

## 內容與範圍證據

- 八份操作文件各自包含 `current`、`historical`、`inference`、`runtime unknown`，以及入口、正常流程、完成判斷、權限／前置、影響／限制、第一個排錯與需求／business-flow 來源。
- Stage 3 已為八份文件內列出的每個 route／頁面補上獨立子流程；每個子流程均交代頁面／欄位或分頁判讀、資料來源／合併邊界、寫入／對外副作用、空資料／部分失敗判讀與 route-specific 第一個排錯。
- `06-訊息素材與群發.md` 已補 `/Richmenu`、`/RichmenuSlave/:masterId/:bindingType` 與 `Richmenu`／`RichmenuSlave` L2 canonical source，並補 `/Audience` 交叉入口、[05-受眾與標籤](../../../docs/msg/operations/05-受眾與標籤.md)、Audience L2 與受眾需求來源。
- `/home/anna/AGENTS.md` 已把完成 handoff 後的可重用 idle Panel 改為預設保留；只關閉無效／stale，或由 coordinator 依容量與清理決策關閉。
- 內容依 CSP operations 的單頁操作邊界整理，並連回 MSG B2E L2 頁面索引、B2E L3 方案索引與既有需求頁；沒有把需求狀態寫成已部署或已送達保證。
- 一般人員與管理者／技術流程邊界已在各頁標示；未加入密碼、Token、完整登入網址、完整客戶名單或其他新敏感資料。
- 其他既有 dirty／untracked 變更未重設、清除或覆寫；本次沒有修改 project-docs、來源快照、程式碼或測試資料。

## Checks

- `git diff --check`：通過。
- Markdown 相對連結檢查：檢查 `docs/msg/README.md`、短索引與 8 份單頁文件，共 10 個檔案、130 個本地連結；缺失 0。
- 文件結構檢查：短索引與 8 份單頁文件共 9 個檔案，必要段落缺失 0。
- Stage 3 route 覆蓋檢查：8 份文件、33 個 route 子流程 heading／route token，獨立子流程缺口 0。
- Stage 3 必要子流程段落檢查：8 份文件的頁面判讀、資料／合併邊界、寫入副作用、空／部分失敗判讀與第一個排錯標記均存在。
- 佔位字串檢查：`TODO`、`TBD`、`placeholder`、`待補`，結果 0。
- `docs/msg/README.md` 與短索引均列出 01–08 八份入口。
- `AGENTS.md` topology 文字檢查：coordinator 主頁、唯一 `WORKERS`、2×2、最多四個 Panel、`WORKERS-<TASK_ID>`、11n／非 11n routing 均存在。

## 限制與未執行的外部操作

- 依使用者最新指示，本回合沒有執行任何 Herdr、`source` 或 Panel 操作，沒有重新派工，也沒有建立獨立 reviewer；因此沒有新增 `review.md` 或 runtime review 證據。
- 未登入 MSG runtime，未驗證目前權限、部署版本、按鈕、資料同步、LINE 送達、直播對外呈現、報表正確性或 AI 費用結果；文件均保留 `runtime unknown` 邊界。
- 未執行 commit、push、deploy、restart、Secret 修改或其他外部服務操作。

FINAL: COMPLETE
