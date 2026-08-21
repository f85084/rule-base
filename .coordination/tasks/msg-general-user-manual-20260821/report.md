# msg-general-user-manual-20260821 writer report

## 交付結果

已完成一般 MSG B2E 使用人員手冊，內容以繁體中文、任務導向方式整理入口、操作順序、完成判斷、前置／權限、可能影響與第一個檢查點；並保留管理者與技術流程邊界。

本任務實際新增或修改的授權檔案：

- `docs/msg/operations/一般人員操作手冊.md`：新增 295 行、24,263 bytes 的一般人員手冊。
- `docs/msg/README.md`：在 `operations/` 索引新增一般人員手冊連結。
- `docs/README.md`：在 MSG「規則與操作說明」新增一般人員手冊連結。
- `.coordination/tasks/msg-general-user-manual-20260821/report.md`：本報告。

沒有修改 `/home/art/openab-repos/project-docs` 的來源文件，也沒有修改 Redmine snapshot、manifest、需求分類、測試、skill 或既有操作文件內容。

## 來源與可追溯證據

- 完整閱讀並遵循 `.coordination/tasks/msg-general-user-manual-20260821/brief.md`。
- 讀取 `/home/art/AGENTS.md` 及其要求的 1:1:N 文件規則；本任務未建立 headless worker、未使用背景命令，也未做外部寫入。
- 讀取 `data/sources/msg/redmine/issues_all.json`：JSON `total_count=532`，`generated_at=2026-08-20T15:30:38+08:00`；專案數為 `OB_message=43`、`message-backend=336`、`message-frontend=153`。抽查 snapshot 的 #50368、#50393 為「新建立」，#50350、#50348、#50346、#50345 為「待測試」，#48499、#46837、#40525、#40508 為「已結束」，並在手冊明確註記需求狀態不等於部署證明。
- 讀取 `data/sources/msg/redmine/summary_all.md`、`docs/msg/requirements/README.md`、`page-classification-index.md`、`page-purpose-index.md` 及本手冊引用的相關 `docs/msg/requirements/pages/*.md`。手冊使用頁面分類與跨頁共用分類的筆數，沒有把需求標題改寫成未驗證的執行承諾。
- 讀取 B2E L2 `INDEX.md` 列出的 31 個具路由頁面文件（不計 `_template.md`），以及 B2E L3 `INDEX.md` 及六份方案文件：登入與安全權限治理、即時客服對話與派線流程、行銷群發與內容素材管理、受眾分群與標籤管理、互動行銷與簽到遊戲管理、直播／統計／費用監控。
- 手冊直接連結六份 L3 方案、所需 L2 頁面與 canonical 需求分類文件；`/multicast` 依來源被標示為非頁面／共用功能，沒有自行捏造單獨的選單分類。

## Scoped checks

1. 本地 Markdown／來源連結檢查：對 `docs/msg/operations/一般人員操作手冊.md`、`docs/msg/README.md`、`docs/README.md` 解析 102 個本地目標；結果為 `checked=102`、`all local targets resolve`。
2. `git diff --check`：通過，沒有 whitespace error。
3. 新增手冊的額外尾端空白檢查：`awk` 掃描無輸出；手冊中的 6 個 L3 檔名、9 個必要任務／邊界標題均逐項檢查為 `PASS`。
4. 敏感資料掃描：對手冊與兩份索引掃描 credential/token/private-key、Bearer、私有網段、HTTP(S) 私有來源與長數字個資樣式；無命中。手冊只保留「不要放入權杖／密碼／個資」的政策提醒，沒有實際秘密值、帳密、權杖、私人網址、SQL 或個人資料。
5. dirty-work／scope 檢查：起始 status 已有 `data/sources/manifest.json`、CSP 文件與測試、MSG 需求分類／Redmine／測試資料、scripts、`.agents/`、`.coordination/` 等 dirty/untracked 工作；完成後 status 保持相同集合，另只增加本任務手冊與本報告。索引的既有 diff 仍保留，未 reset、checkout、clean、刪除或覆寫其他檔案。

## 限制與未驗證事項

- 沒有登入實際 MSG 環境、開啟瀏覽器、執行任何頁面操作或驗證目前角色權限；手冊中的權限與部署狀態均依來源描述並標示為環境相關。
- 沒有把 Redmine 的「已結束／待測試／新建立」解讀為已上線或已驗收；尤其簽到相關近期需求仍以 snapshot 狀態呈現。
- B2E L2/L3 文件是業務流程與頁面來源描述，不能取代 runtime config、現行公告、權限矩陣或外部 LINE 平台結果。
- 手冊刻意不提供 API、Controller、資料庫、Webhook、JOB、SignalR、Token、SQL、私有環境或完整個資內容；技術排查仍需交給管理者／維運。

## 未執行的外部操作

- 未執行 commit、push、merge、部署、服務重啟或任何 Git 寫入。
- 未寫入 Redmine、Wiki、MSG runtime、資料庫、外部 LINE 平台、秘密管理系統或其他外部服務。
- 未使用帳號、密碼、權杖或私有環境連線；未修改 `/home/art/openab-repos/project-docs` 的來源文件。

Status: COMPLETE
