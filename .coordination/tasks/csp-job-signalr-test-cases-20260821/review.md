# Follow-up review：CSP Job #50285／#50152 SignalR 解耦

## Stage 3 修正核對

本次只讀核對 Stage 3 的案例文件與 writer report 修正，未執行 Herdr、`source`、Job／API／CI、Redis／SignalR／瀏覽器 runtime、外部服務或任何 runtime mutation。

原 Finding 1 已解決：

- `docs/csp/test-cases/test-cases-50285-50152-job-signalr-decoupling.md:262` 現為 `../../../data/sources/csp/redmine/issues_all.json`。
- 從 `docs/csp/test-cases/` 解析後，目標 canonical source 存在且可讀；兩份 operations 連結與 README 入口也可解析。
- `report.md:38-39` 的 whitespace／連結檢查描述與本次實際結果一致。

原 Finding 2 已解決：

- `TC-COM-01` `docs/csp/test-cases/test-cases-50285-50152-job-signalr-decoupling.md:246-247` 已限定檢查 `HubConnection`、`Microsoft.AspNetCore.SignalR.Client`、SignalR connection 的 Hub invocation，並明確排除泛用 `apiInvoker.InvokeAsync`、`SyncTmListApiInvoker`、`PushMessageApiInvoker` 與其他 HTTP invoker。
- 因此不會再以單獨的 `InvokeAsync` 字串判定 path-level SignalR 依賴；project-level package 仍獨立盤點。

原 Finding 3 已解決：

- `TC-50152-07` `:222-233` 已要求使用核准的 automation／integration stub 或只作用於合成 receiver id 且可回復的 Lab fixture。
- 步驟已包含啟用方式、run／fixture 識別、時間與負責人、停用／清理、恢復驗證，以及無 stub／fixture 能力時標示 automation-only／待建立 fixture 並停止直接 runtime 操作的邊界。

目前沒有未解決 finding。

## 通過項目

- #50285／#50152 的正常、錯誤、重試、JWT、HTTP、Redis／SignalR reconnect、前端回歸，以及 path-level／project-level SignalR 邊界仍完整覆蓋。
- #50152 的批次 50、pending-only、transient retry 最多 3 次、400 不重試與 `FailedReceivers` contract，及 #50285 的非 2xx warning／下一排程週期續行，均維持來源對齊。
- 每個案例仍具備 ID、優先級／類型、前置條件、測試資料、步驟、預期、證據與通過判定；Redis replay 未定義部分沒有被寫成保證。
- #50285 不在本地 Redmine 快照的限制仍誠實標示；runtime 未執行也仍明確標為待 QA 執行，未把靜態或 automation evidence 宣稱為 runtime 通過。
- Stage 3 未引入實際帳密、token、secret、私有連線字串、個資或未由來源支持的固定 UI／資料。

## Checks

- Redmine 連結以 `docs/csp/test-cases/../../../data/sources/csp/redmine/issues_all.json` 實際檢查存在；README、兩份 operations 與案例入口均可解析。
- `git diff --check` 無 whitespace error；案例文件、report 與 README 的 untracked diff check 未輸出 whitespace error。untracked diff 的非零差異狀態未被誤報為 whitespace failure。
- `report.md:38-40` 所列 Stage 3 checks 與實際一致：連結修正可解析、無 whitespace error，且 runtime／CI／外部服務均未執行。
- `review.md` 目前只保留本文最後一個 reviewer marker；report 仍只保留一個 writer completion marker，案例與 README 沒有額外 marker。
- Stage 3 期間未發現 backend source 變更；rule-base 其餘 modified／untracked work 為既有工作，未 reset、checkout、清理或覆寫。README／brief 未見 Stage 3 修改；Stage 3 變更限於授權的案例文件與 report。

## 限制

- 本 follow-up 仍未執行 runtime，因此不能替 QA 判定 HTTP endpoint、JWT 實際驗證、Redis／SignalR reconnect、FATAL absence 或瀏覽器即時更新已通過。
- 本 review 只驗收 Stage 3 文件修正，不代表整體產品或部署 acceptance 已完成。

## Stage 4 follow-up：一般人員／PO 功能驗收版

- 審查文件：docs/csp/test-cases/test-cases-50285-50152-job-signalr-decoupling.md。
- 案例數核對：#50285 四案、#50152 四案、共同回歸一案，共 9 案。
- 欄位核對：9 案均有測試目的、測試角色、開始前準備、操作步驟、預期結果、通過判定、結果記錄。
- 可讀性核對：操作以一般人員／PO 看畫面為主；維運協助只準備合成資料與必要背景動作；不要求測試者操作 Job、查看技術紀錄或敏感資訊。
- 情境核對：已涵蓋名單同步、無新資料、指定回電／客訴未結、離線再登入、新訊息提醒、多人資料不混淆、短暫斷線恢復、異常資料後下一筆正常訊息。
- 技術邊界核對：案例正文沒有要求 API、JWT、Redis、SignalR、stub、HTTP status、程式碼、package 或技術 log 操作；文件明確區分功能驗收與技術驗收。
- Checks：案例檔與 report 的 untracked diff check 無 whitespace error；runtime、source、CI、外部服務未執行，未宣稱 runtime 通過。

Stage 4 review 結論：案例文件符合一般人員／PO 功能驗收需求。

## Stage 5 follow-up：Excel 填寫版

- xlsx 已存在，並以 Python 標準庫 `zipfile.testzip()` 與 XML parser 檢查通過；三個工作表為「測試總覽」「測試案例」「填寫說明」。
- 測試總覽與測試案例各有 9 筆資料，案例 ID 與 Markdown 一致：#50285 四案、#50152 四案、共同回歸一案。
- 測試案例欄位完整：案例 ID、需求單、測試目的、測試角色、開始前準備、操作步驟、預期結果、通過判定、執行結果、測試日期、測試人員、證據／備註；執行結果預設待 QA 執行。
- XML 可確認凍結首列、autoFilter、wrapText 與結果下拉選項；README Excel 入口存在；未發現帳密、token、個資或技術操作。
- runtime、source、CI、外部服務未執行。

Stage 5 review 結論：Excel 可交給一般人員／PO 填寫。

## Stage 5 correction follow-up

- QA 回報 sheet1／sheet2 XML 載入錯誤；已確認原因為 `autoFilter` 與 `dataValidations` 元素順序不符合 Excel 工作表 XML 要求。
- 修正後重新確認 xlsx ZIP 完整性、三個工作表 XML 可解析，且 sheet1／sheet2 的 `autoFilter` 排在 `dataValidations` 前方。
- 測試案例資料與 9 案內容未變更；runtime 仍未執行。

FINAL: APPROVED
