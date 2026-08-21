# manual-site-msg-prototype-20260821 Stage 2 reviewer re-review

## 審查範圍與環境

唯讀檢查 `brief.md`、`report.md`、`docs/manual-site/**`、canonical `docs/msg/operations/02-聊天室與客服.md`，以及 static/source duplication/scope/diff checks。未修改 writer 檔案、brief、report 或任何來源；未 commit、push、deploy。

- 從 rule-base root 啟動 `python3 -m http.server 8765 --bind 127.0.0.1`，測試 `http://127.0.0.1:8765/docs/manual-site/`，完成後正常停止。
- Python Playwright `1.62.0`；Chromium `151.0.7922.34`；executable `/home/anna/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome`。
- 啟動 Chromium 前使用 `LD_LIBRARY_PATH=/home/anna/.local/share/manual-site-libs/root/usr/lib/x86_64-linux-gnu`；此為 user-local workaround，未安裝或修改系統套件。

## Findings

無 acceptance finding。先前的搜尋可見性與預期結果拆分問題已由 writer 修正並在本次 browser runtime 驗證通過。

## Browser runtime 證據

- 首頁 HTTP 200，URL 為指定 loopback URL，title 為 `MSG Manual Site Prototype`；首頁 `#load-error` 不可見，canonical source chip 為 `docs/msg/operations/02-聊天室與客服.md`。
- canonical source body 顯示 `02 聊天室與客服`，source path link 指向同一 canonical Markdown；source status 保留 `current source · runtime UI 未驗證`，沒有把本次本機檢查宣稱成 production runtime。
- 無命中搜尋 `zz-no-hit-20260821` 時，3 個 nav items 的 `hidden` property 均為 true 且均不可見；命中 `RedirectToChatroom` 時，`msg-chat` 可見，其餘未命中 items 不可見，搜尋訊息顯示 1 個命中。
- 首頁有 3 張 `.step-card` 與 3 個 expected blocks；每張卡片的 expected 均獨立呈現，沒有「來源未提供獨立預期結果／待補」，action 文字也不再包含原始 `預期結果` 標籤。canonical source `docs/msg/operations/02-聊天室與客服.md:11-13` 的三個結果均正確拆出。
- 點擊 `msg-operations-index` 後成功切換為「MSG 一般人員操作手冊」，source chip 更新為 `docs/msg/operations/一般人員操作手冊.md`，`#load-error` 不可見，目標 nav button 的 `aria-current` 為 `page`。
- FAQ details 初始開啟，點擊後關閉並可重新開啟；technical details 初始收合，點擊後開啟並可重新收合。
- Playwright `pageerror` 為空；首頁與導覽切換後的 `#load-error` 均不可見。唯一 console error 是靜態原型未提供 favicon 造成的 `/favicon.ico` HTTP 404，未影響頁面或 brief 指定功能，列為非阻塞限制。

## Static、source、scope 與 diff 證據

- `styles.css:18` 已加入 `[hidden] { display: none !important; }`；`app.js:187-189` 的 `splitExpected()` 可處理句號後直接接 `預期結果：`／`預期結果:`。
- `nav.json` JSON 可解析，共 3 個 documents，`defaultDocument` 為 `msg-chat`，所有非 null source path 均存在；`index.html:8`、`:130` 的 CSS／JS 引用存在，README 引用存在。
- source duplication guard 未在 `docs/manual-site/**` 找到 canonical 02 長正文副本；正文仍由 `app.js:264-284` runtime fetch，並在 `app.js:251` 渲染。
- `git diff --check` 通過；對目前 untracked manual-site／report 的 trailing-whitespace check 無結果。`git status --short -- docs/msg docs/csp project-docs` 無輸出，scope 外來源未被修改；目前 workspace 的 task／manual-site untracked paths 與既有 dirty work 保留。
- report 的 checks 已記錄 Stage 3 修正與 Playwright evidence；`report.md:46` 僅有一個 report marker，值為 `READY FOR REVIEW`。本次未修改 report。

## 未確認限制

- 本次為 headless Chromium 的本機 static-server 檢查；不代表 production、auth、roles、write、LINE 送達、部署或外部服務 runtime。
- `/favicon.ico` 未提供而回傳 404；這是非 brief acceptance 的資產缺口，未造成 app page error。
- 未執行 Herdr、Panel、source、runtime mutation、commit、push、deploy 或其他外部操作。

FINAL: APPROVED
