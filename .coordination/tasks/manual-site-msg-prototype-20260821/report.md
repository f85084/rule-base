# manual-site MSG 聊天室與客服原型 Writer Report

## 實際修改檔案

只新增 brief 授權範圍內的檔案：

- `docs/manual-site/index.html`
- `docs/manual-site/styles.css`
- `docs/manual-site/app.js`
- `docs/manual-site/nav.json`
- `docs/manual-site/README.md`
- `.coordination/tasks/manual-site-msg-prototype-20260821/report.md`

既有 dirty／untracked 工作保留，沒有修改 `docs/msg/**`、`docs/csp/**`、`project-docs/**`、程式碼或來源文件。

## 內容與 canonical sources

- 先盤點既有 dirty 狀態；task 開始時目標網站目錄不存在，既有 task 目錄只含 brief。
- 讀取 `/home/art/AGENTS.md`、`/home/anna/AGENTS.md`、`project-docs/AGENTS.md` 與 `project-docs/projects/MSG/AGENTS.md`。
- 讀取 `docs/msg/README.md` 與 canonical `docs/msg/operations/02-聊天室與客服.md`。
- 讀取該操作頁明確連結的 MSG business-flow sources：
  - `project-docs/projects/MSG/data/business-flows/B2E/L2/ChatRoom-頁面全貌.md`
  - `project-docs/projects/MSG/data/business-flows/B2E/L2/RedirectToChatroom-頁面全貌.md`
  - `project-docs/projects/MSG/data/business-flows/B2E/L3/即時客服對話與派線流程.md`
- 原型以 `nav.json` 保存標題、分類、route、canonical source path 與狀態；正文由 `app.js` 在瀏覽器執行期 fetch，不複製到 `docs/manual-site/**`。
- 首頁優先呈現 `/chat/:uuid` 的「聊天室與客服」，並提供 `/RedirectToChatroom/:customerId` 脈絡、MSG 操作手冊索引入口與 CSP 後續擴充 placeholder。
- UI 具備側欄導覽、關鍵字搜尋、由來源編號步驟產生的操作卡、預期結果、完成確認、FAQ／第一個排錯、可收合來源正文與技術／狀態附錄；來源沒有獨立段落時顯示「來源未提供／待補」。
- 畫面明確標示 `current source` 與 `runtime unknown`；沒有把需求、來源或本機載入結果寫成已部署或外部送達保證。

## Checks

- `git diff --check`：通過。
- HTML 資產引用、JSON manifest、manifest source path 與 CSS brace 基本檢查：通過。
- source duplication guard：通過；`docs/manual-site/**` 沒有 canonical ChatRoom 的正文／API 表格識別內容。
- 本機 static server HTTP runtime：通過。以 `python3 -m http.server 8765 --bind 127.0.0.1` 從 repository root 服務，確認首頁、`nav.json`、`app.js`、`styles.css` 與 `docs/msg/operations/02-聊天室與客服.md` 可由 HTTP 載入；首頁 title、fetch source 程式與 canonical Markdown 標題均命中。
- Stage 3 CSS 修復：在 `styles.css` 加入 `[hidden] { display: none !important; }`，避免 `.nav-item { display: grid; }` 覆蓋搜尋結果的 hidden 屬性，保留原有導覽版面。
- Stage 3 JS 修復：`splitExpected()` 改以 `預期結果：`／`預期結果:` 標籤拆分，不再要求標籤前有空白，因此可解析 canonical 來源中句號直接相接的既有結果；沒有改寫或複製 canonical Markdown。
- Playwright＋Chromium runtime：通過。以已安裝 Chromium 與 `LD_LIBRARY_PATH=/home/anna/.local/share/manual-site-libs/root/usr/lib/x86_64-linux-gnu` 載入本機 static server；確認 3 張 `.step-card` 都有獨立預期結果且沒有「來源未提供獨立預期結果／待補」、無命中搜尋時所有 nav item 隱藏、命中搜尋時目標項目可見、技術附錄可開／收合，且沒有 page error。
- standalone JavaScript syntax command：未執行；環境沒有 `node`、`deno`、`bun` 或 `qjs`，但本次 Playwright／Chromium 已實際執行並載入 `app.js`。

## 限制與未執行的外部操作

- 這是無外部依賴的靜態原型，不實作登入、角色控管、資料寫入、公開發布、production API、LINE 送達驗證或部署整合。
- 從 repo root 以 `file://` 開啟會使瀏覽器阻擋 fetch；請依 `docs/manual-site/README.md` 啟動本機靜態伺服器。
- repo 外的 `project-docs` 來源只作 canonical context／連結脈絡；本原型不把它們複製到網站，也不宣稱靜態伺服器已提供所有 repo 外連結。
- 未執行 Herdr 派工、reviewer 操作、commit、push、deploy、Secret 變更、外部服務查詢或 production runtime 操作；本次僅使用本機 static server 與 Playwright／Chromium 驗證原型。

FINAL: READY FOR REVIEW
