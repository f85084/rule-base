# Bounded Brief：manual-site MSG 聊天室與客服原型

## 目標

在 `rule-base/docs/manual-site/` 建立可本機預覽的、依現有 Markdown 來源即時載入的手冊網站原型，優先呈現 MSG「聊天室與客服」操作手冊，並提供後續擴充 MSG／CSP 的導航骨架。

## 角色與交接

- **唯一 writer**：一名共享 `WORKERS` 頁籤中的可見、互動式 `codex` worker。
- **獨立 reviewer**：writer 完成 `report.md` 後，使用同一 `WORKERS` 頁籤的另一個可見、互動式 Panel 唯讀檢查，寫入 `review.md`。
- **coordinator**：依 report、review、workspace diff 與 checks 做 acceptance；未經明確授權不部署、不修改 Secret、不推送外部服務。

## 工作範圍

只修改以下範圍：

- `docs/manual-site/**`
- `.coordination/tasks/manual-site-msg-prototype-20260821/report.md`
- 必要時在同一 task 目錄補充 writer 產出的證據檔，但不得把來源文件複製成第二份內容。

### 必須完成

1. 建立能以簡單本機靜態伺服器預覽的網站骨架，避免引入不必要的外部依賴。
2. 由瀏覽器執行期直接 fetch 現有 Markdown 來源；操作手冊正文不得複製到 `manual-site`。允許建立只含路徑、標題、分類與來源連結的 navigation manifest。
3. 優先呈現 `docs/msg/operations/02-聊天室與客服.md`，保留來源標題、段落、清單、表格、程式碼與連結的可讀性。
4. 提供首頁／側欄導覽、關鍵字搜尋、操作步驟卡片、預期結果、常見問題，以及可收合的技術附錄或來源資訊；若來源未提供某項內容，必須標示「來源未提供／待補」，不得自行捏造業務規則。
5. 顯示 canonical source 路徑與來源狀態，區分現行來源內容、推論與待確認事項；不宣稱已完成 runtime 驗證。
6. 補上本機啟動與維護說明，讓後續 worker 能加入其他 MSG／CSP 文件而不改變單一資料源原則。

## 排除事項

- 不修改 `docs/msg/**`、`docs/csp/**`、`project-docs/**` 的既有來源文件。
- 不在本 task 實作登入、權限控管、公開發布、Vercel／GitHub Pages／Sites 部署或 production runtime 整合。
- 不自行補寫來源沒有支持的 API、權限、保存期限、成功保證或錯誤處理契約。
- 不新增大型 framework、build pipeline 或需要網路安裝的依賴；若確有必要，先在 report 說明理由與限制。
- 不處理 Redmine、dev-deploy、#50368 或其他待辦主題。

## 唯一事實來源

- `rule-base/docs/msg/operations/02-聊天室與客服.md`
- `rule-base/docs/msg/README.md`
- 該操作手冊明確連結的 MSG requirements／business-flow 文件，僅作來源連結與脈絡，不複製正文。
- 網站的 UI 行為以本 brief 與現有來源為準；對未確認內容標示狀態。

## 檢查要求

- `git diff --check`。
- 對 JavaScript 執行可用的語法檢查；對 HTML／CSS 做基本檔案與引用檢查。
- 使用本機靜態伺服器實際載入首頁與 `02-聊天室與客服.md`，確認 fetch 成功、Markdown 可呈現、搜尋與收合互動可用；不得只以檔案存在代替 runtime 檢查。
- 檢查網站未把 MSG 操作手冊正文重複寫入 `docs/manual-site/**`。

## 驗收條件

- `docs/manual-site/` 可啟動並顯示原型。
- MSG「聊天室與客服」正文來自執行期載入的 canonical Markdown，且顯示來源連結／路徑。
- 首頁導覽、搜尋、步驟卡片、預期結果、FAQ、技術附錄收合均可操作；缺來源內容時有明確待補標記。
- writer 已完成 `.coordination/tasks/manual-site-msg-prototype-20260821/report.md`，列出實際檔案、checks、限制與未執行的外部操作，且只有一個 final marker。

## 完成標記與交接

writer report 最後只能保留一個：

`FINAL: READY FOR REVIEW`

reviewer 另於 `review.md` 使用自己的唯一 final marker；writer 不得代寫 reviewer 結果。
