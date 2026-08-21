# Writer report：CSP Job SignalR 解耦測試案例

## 目標

新增可交給 QA 執行的繁體中文測試案例，涵蓋 CSP #50285／#50152 的正常、錯誤、重試、JWT、HTTP endpoint、Redis／SignalR 重連、前端即時更新與架構依賴驗收；明確區分來源證據與 runtime 未執行範圍。

## 實際修改檔案

- docs/csp/test-cases/test-cases-50285-50152-job-signalr-decoupling.md
  - 新增 #50285、#50152、共同回歸與架構檢查案例。
  - 每個案例列出 ID、優先級／類型、前置條件、測試資料、步驟、預期結果、證據與通過判定。
  - 明確標示本次未執行 Job、HTTP、Redis、SignalR、瀏覽器與外部服務 runtime。
  - 避免寫入帳密、JWT、secret、連線字串、個資及未由來源支持的固定保證。
- docs/csp/test-cases/README.md
  - 新增 #50285／#50152 測試案例索引入口。
- .coordination/tasks/csp-job-signalr-test-cases-20260821/report.md
  - 本 writer report。

未修改程式碼、設定、既有測試資料、brief、review.md 或其他文件；未 commit、push、deploy、restart、改 Secret 或呼叫外部服務。

## 來源與限制

- 已讀 /home/anna/AGENTS.md、/home/art/AGENTS.md、task brief、brief 列出的 Job／API／測試／CSP 文件與相關目錄規則。
- 本地 Redmine 快照有 #50152，沒有 #50285；#50285 文件內容僅採用 task brief／使用者明示範圍，沒有虛構快照外的需求細節。
- 現行 source 顯示兩個指定 Job path 以 HTTP API 為出口，API 端仍可能用 IHubContext 推送瀏覽器；Job 專案仍有其他工作使用 SignalR Client 的 project-level 套件，因此報告與案例把 path-level 解耦和 project-level package removal 分開驗收。
- #50285 非 2xx 在目前 TmListJobApiClient 會記錄 warning；來源沒有 per-call 三次重試，因此案例明確要求驗證「下一排程週期續行」而非虛構立即重試。
- Redis Pub/Sub 斷線期間的訊息 replay／保留契約未由來源定義，案例只把「恢復後新訊息可繼續處理」列為可驗收結果，並要求將斷線期間訊息另依正式可靠度契約判定。

## Stage 3 修正與證據

- Finding 1：將案例文件第 258 行的 Redmine 快照連結由 ../../data/sources/csp/redmine/issues_all.json 修正為 ../../../data/sources/csp/redmine/issues_all.json；由 docs/csp/test-cases/ 解析至 canonical data/sources/csp/redmine/issues_all.json。
- Finding 2：將 TC-COM-01 的架構搜尋限定為 HubConnection、Microsoft.AspNetCore.SignalR.Client、SignalR connection 的 InvokeAsync／Hub client invocation；明確排除 SyncTmList／PushMessage 的 apiInvoker.InvokeAsync、SyncTmListApiInvoker、PushMessageApiInvoker 與其他 HTTP invoker；project-level package 仍獨立盤點。
- Finding 3：為 TC-50152-07 receiver2 部分失敗補上核准 automation／integration stub 或只對合成 receiver id 生效且可回復的 Lab fixture；案例要求記錄啟用、run／fixture 識別、清理與恢復驗證。若環境沒有能力，明確標示 automation-only／待建立 fixture，禁止直接假設可執行。
- Stage 3 仍未執行 source、Herdr、runtime、外部服務或任何 fault injection；只做案例文件與 report 的文字修正。

## Checks

- git diff --check：Stage 3 修正後已執行，無 whitespace error；另對案例文件與 report 執行 git diff --no-index --check，無 whitespace error。
- Markdown 相對連結與 README 入口：Stage 3 修正後已重新執行；案例文件的兩份 operations 連結、修正後 Redmine 連結、README 的既有入口與案例文件入口均可解析。README 未修改。
- runtime：未執行。未執行項目包含 Job、API endpoint、JWT 實際驗證、Redis publish／reconnect、SignalR reconnect、瀏覽器即時更新、CI／dotnet test 與任何外部服務。

## Stage 4 修正與證據

- 已將案例文件改寫為一般員工／PO 可直接依畫面執行的功能驗收版本。
- 實際案例數為 9 案：#50285 四案、#50152 四案、共同回歸一案。
- 每案只保留測試目的、測試角色、開始前準備、操作步驟、預期結果、通過判定、結果記錄七欄。
- 已移除一般測試者的技術操作與技術判讀；維運協助只準備合成資料、安排必要背景動作與清理，不要求測試者操作背景工作或查看技術紀錄。
- 文件開頭明確標示功能驗收與技術驗收分工，並標示目前狀態為待 QA 執行；未宣稱任何 runtime 通過。

## Stage 4 Checks

- git diff --check：已執行，無 whitespace error；案例文件與 report 另以 git diff --no-index --check 檢查，無 whitespace error。
- 必要檔案存在檢查：已執行，案例文件與 report 均存在；案例共 9 案（#50285 四案、#50152 四案、共同一案）。
- runtime、source、Herdr、commit、push、deploy 與外部服務：未執行。

## Stage 5 Excel 交付與證據

- 新增 `docs/csp/test-cases/test-cases-50285-50152-job-signalr-decoupling.xlsx`，依既有 9 個一般人員／PO 案例建立三個工作表：測試總覽、測試案例、填寫說明。
- Excel 的測試案例工作表每案一列，包含案例 ID、需求單、測試目的、測試角色、開始前準備、操作步驟、預期結果、通過判定、執行結果、測試日期、測試人員、證據／備註；執行結果預設為待 QA 執行。
- Excel 已加入凍結標題列、篩選、換行、欄寬、標題樣式與結果下拉選項，未放入帳密、token、個資或技術操作。
- `docs/csp/test-cases/README.md` 已加入 Excel 填寫版入口。

## Stage 5 Checks

- xlsx 檔案存在；因環境沒有 `unzip` 指令，改以 Python 標準庫 `zipfile.testzip()` 與 XML parser 做等效完整性檢查，確認包含 3 個工作表 XML、workbook 與 styles。
- 從 Markdown 解析案例數為 9 案：#50285 四案、#50152 四案、共同回歸一案；Excel 測試案例資料列同為 9 案。
- `git diff --check` 與 xlsx／README／report 的 untracked diff check 無 whitespace error。
- runtime、source、CI、外部服務、commit、push、deploy：未執行。

## Stage 5 相容性修正

- QA 回報 Excel 開啟時 sheet1／sheet2 XML 載入錯誤；原因為補入篩選標記後，`autoFilter` 排在 `dataValidations` 後方，不符合工作表 XML 元素順序。
- 已修正 `xl/worksheets/sheet1.xml` 與 `sheet2.xml` 的元素順序，未改變測試案例內容。
- 修正後重新以 Python `zipfile.testzip()`、XML parser 及元素順序檢查，三個工作表均可解析，且 `autoFilter` 位於 `dataValidations` 前方。

FINAL: COMPLETE
