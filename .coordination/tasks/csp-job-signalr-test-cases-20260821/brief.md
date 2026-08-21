# CSP Job SignalR 解耦測試案例 brief

## 目標

為 MoneyIn Redmine #50285 與 #50152 建立可交給 QA／主管執行的繁體中文測試案例，涵蓋功能結果、錯誤處理、重試、認證與移除 SignalR 依賴的回歸驗收。

## 唯一 writer 與 reviewer

- Writer：一名可見、互動式 worker，負責新增測試案例文件與索引入口。
- Reviewer：同 task 頁籤內另一個可見、互動式 worker，唯讀檢查需求覆蓋、步驟可執行性、預期結果、證據與敏感資料。

## 授權修改範圍

- `/home/art/openab-repos/rule-base/docs/csp/test-cases/test-cases-50285-50152-job-signalr-decoupling.md`
- `/home/art/openab-repos/rule-base/docs/csp/test-cases/README.md`
- `/home/art/openab-repos/rule-base/docs/csp/test-cases/test-cases-50285-50152-job-signalr-decoupling.xlsx`
- `/home/art/openab-repos/rule-base/.coordination/tasks/csp-job-signalr-test-cases-20260821/brief.md`
- `/home/art/openab-repos/rule-base/.coordination/tasks/csp-job-signalr-test-cases-20260821/report.md`
- `/home/art/openab-repos/rule-base/.coordination/tasks/csp-job-signalr-test-cases-20260821/review.md`

不得修改程式碼、設定、既有測試資料、其他文件或外部服務；保留 workspace 既有 dirty／untracked 變更。

## 事實來源

- Redmine 匯出：`data/sources/csp/redmine/issues_all.json`（#50152）；#50285 標題由使用者提供，若本地快照沒有該單，不得虛構未提供的需求細節。
- 現行 Job：`/home/art/openab-repos/customer-service-backend/Ehs.CustomerService.Job/Core/SyncTmList.cs`、`PushMessage.cs`。
- 現行 Job API client／token：`Ehs.CustomerService.Job/Core/Services/TmListJobApiClient.cs`、`SyncTmListTokenProvider.cs`、`PushMessageJobApiClient.cs`。
- 現行 API endpoint／service：`Ehs.CustomerService.API/Aggregates/TelephoneMarketing/TmListJobController.cs`、`TmListSyncService.cs`、`MessageJobController.cs`、`MessagePushService.cs`。
- 現有自動化證據：`Ehs.CustomerService.Test/Aggregates/Message/PushMessageJobTests.cs`、`TelephoneMarketing/TmListSyncEntryPointTests.cs`。
- CSP 操作／排程說明：`rule-base/docs/csp/operations/04-TM名單推薦.md`、`50-排程工作狀態.md`。

## 文件要求

- 清楚區分 #50285、#50152、共同回歸與架構驗收。
- 每個案例至少有：案例 ID、優先級／類型、前置條件、測試資料、操作步驟、預期結果、應留存證據、通過判定。
- 覆蓋：正常同步／推播、空資料、部分失敗、HTTP 非 2xx、timeout／5xx／429 重試、取消、JWT 缺少或錯誤 claim、錯誤 endpoint、SignalR／Redis 異常期間不產生 FATAL、恢復後可繼續處理、既有前端即時更新回歸。
- #50285 必須驗證 Job 呼叫 HTTP API 而非 TMList SignalR Hub，且同步結果仍能送達專員、指定回電／客訴未結通知邏輯不退化。
- #50152 必須驗證 Job 呼叫 MessageJob HTTP API 而非 SignalR `InvokeAsync`，Redis 訊息不因連線重連造成 `InvalidOperationException`／FATAL；需說明如何在 Lab 取得可觀察證據，不得宣稱未執行的 runtime 結果。
- 不寫入帳密、token、私有連線字串、個資或未由來源支持的固定 UI／資料保證；runtime 未確認處明確標示為待執行。

## 檢查與交接

- `git diff --check`
- Markdown 相對連結與索引入口可解析。
- 文件中只保留一個 `FINAL: COMPLETE`；report 列出實際檔案、checks、限制與未執行的外部操作。
- reviewer 只寫 review.md，最後只保留一個 `FINAL: APPROVED`、`FINAL: NEEDS REVISION` 或 `FINAL: BLOCKED`。

## Stage 5 Excel 交付追加

- 依已核准的 9 個一般人員／PO 功能驗收案例建立 Excel 版，供測試時直接填寫。
- Excel 至少包含「測試總覽」與「測試案例」工作表；案例欄位包含案例 ID、需求單、測試目的、測試角色、開始前準備、操作步驟、預期結果、通過判定、執行結果、測試日期、測試人員、證據／備註。
- 不新增技術操作、敏感資料或未執行 runtime 的通過宣稱；預設結果為「待 QA 執行」。
- Excel 只可由 writer 建立；reviewer 唯讀檢查工作表、案例數、欄位、可填寫性與敏感資料，並更新 review.md。
