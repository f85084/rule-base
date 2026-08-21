# Bounded brief: manualize MSG/CSP operations

## Objective

將目前 `docs/msg/operations` 與 `docs/csp/operations` 中面向一般人員的內容，改寫成可由第一次使用者照著畫面完成工作的操作手冊。主文必須回答「從哪裡進入、要按什麼、看到什麼算成功、出錯先做什麼」，不可再以需求摘要、route 清單、資料來源說明或維運查核作為主要閱讀順序。

## Roles

- Coordinator：主協調者，負責範圍、交接與最終驗收。
- Writer：唯一文件修改者，使用既有 `WORKERS` 頁籤的 `w1:p18`，完成後寫本 task 的 `report.md`。
- Reviewer：獨立唯讀 reviewer，使用既有 `WORKERS` 頁籤的 `w1:p19`，完成後寫本 task 的 `review.md`；不得修改 writer 文件。

## Scope

### Must change

- `docs/msg/operations/一般人員操作手冊.md`
- `docs/msg/operations/01-登入與帳號.md` 至 `08-查詢統計與直播.md`
- `docs/csp/operations/` 內直接面向一般客服／操作人員的入口與頁面手冊；優先處理 `日常作業.md`、`客戶服務.md`、`接單與訂單.md`、`訊息查詢與通知中心.md`、`軟體電話.md`、`商品與特殊接單.md`、`LINE綁定與AI助手.md`、`04-TM名單推薦.md`、`05-客戶查詢.md`、`06-接單作業.md`、`07-訂單管理.md`、`09-客訴處理.md`、`12-聯繫歷史.md`、`13-電話小結作業.md`、`14-客服員待辦事項.md`、`17-票劵-預約.md`、`18-直播-見面會報名.md`、`19-商品訊息.md`、`20-訊息查詢.md`、`21-通知中心.md`、`22-調聽音檔.md`、`24-訂單質檢.md`、`26-質檢查詢.md`、`28-客戶進階查詢.md`、`29-客服即時狀態.md`、`30-客服文件管理.md`、`37-直播-見面會管理.md`、`38-行事曆.md`、`47-小結清單.md`。

### May leave unchanged unless needed for navigation consistency

- 純管理者、系統維運、AI 設定、Domain、排程、外部服務紀錄等頁面；不可為了改版而刪除或覆寫其既有內容。
- `MI完整手冊.md`、`MI維運操作入口.md` 等大型維運文件；只需確保一般人員入口不把技術維運內容當成主要操作步驟。

## Writing contract

每份面向一般人員的頁面手冊，依實際證據使用以下順序；若某項沒有證據，標示「目前資料未確認」，不得自行捏造按鈕或欄位：

1. 這頁是做什麼：適用角色、何時使用、進入路徑／頁面名稱。
2. 開始前：必要帳號、權限、資料或前置狀態。
3. 照著做：以編號步驟呈現「畫面位置／操作／預期結果」，使用實際可見的按鈕、欄位、頁籤、提示文字；能辨識多個任務時，分成查詢、新增、編輯、送出、結案等任務。
4. 完成確認：一般人員可自行判斷的成功條件與不可漏看的狀態。
5. 常見問題：以「看到什麼 → 先做什麼 → 仍失敗找誰／提供什麼資訊」呈現。
6. 影響與提醒：會寫入、送出、轉派、通知、扣庫存或不可逆的動作，放在操作步驟附近。
7. 來源與技術補充：需求單、business-flow、API／資料表／cache 等放在文末附錄，不得打斷一般操作流程。

## Quality bar

- 不以 `current/historical/inference/runtime unknown`、route 索引或來源清單作為開頭主體。
- 不用「依流程處理」「檢查相關欄位」「確認成功」等無法執行的抽象句取代實際操作；若實際 UI 標籤未知，明確保留待確認項目。
- 一般人員不需要理解 API、資料表、merge、cache 才能讀懂主文。
- 保留既有 dirty／untracked work；只改本 brief 授權的文件與本 task 證據檔，不得 reset、checkout、刪除或覆寫無關內容。
- 不新增截圖或虛構畫面；若 repository 沒有可引用的畫面證據，先用文字步驟並列出待補截圖清單。

## Checks

- 檢查所有改寫文件的標題、入口、角色、步驟、預期結果、完成條件與錯誤處理是否存在。
- `git diff --check`。
- 檢查內部連結與檔名是否仍可解析；不要因無法執行外部系統而聲稱 runtime 驗證完成。

## Handoff

- Writer：完成文件後寫 `/home/art/openab-repos/rule-base/.coordination/tasks/manualize-msg-csp-operations-20260821/report.md`，只保留一個 `FINAL: COMPLETE`。
- Reviewer：讀取 brief、writer report、精確 diff 與檢查輸出，唯讀檢查後寫 `/home/art/openab-repos/rule-base/.coordination/tasks/manualize-msg-csp-operations-20260821/review.md`，只保留一個 `FINAL: APPROVED` 或 `FINAL: NEEDS REVISION`。
- Coordinator：只有收到 report 與 review 後才做 workspace、diff、dirty preservation、文件同步與限制的最終驗收；未授權 commit、push、deploy。
