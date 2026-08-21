# Manual Site 原型

這是 MSG／CSP 操作手冊的本機靜態網站原型。原型優先呈現 MSG「聊天室與客服」，操作手冊正文不複製到 `docs/manual-site/`，而是由瀏覽器執行期從 canonical Markdown `docs/msg/operations/02-聊天室與客服.md` 載入。

## 本機預覽

在 `rule-base` repository root 啟動簡單靜態伺服器：

```bash
python3 -m http.server 8000
```

再開啟 <http://127.0.0.1:8000/docs/manual-site/>。不要直接以 `file://` 開啟 `index.html`，否則瀏覽器會阻擋 `fetch` 來源 Markdown。

## 結構與資料來源

- `index.html`：網站 shell、首頁／側欄／搜尋／操作摘要與可收合附錄的容器。
- `styles.css`：無外部依賴的 responsive 樣式。
- `app.js`：原生 JavaScript Markdown 輕量呈現器；只負責顯示來源，不承擔登入、權限或 production API。
- `nav.json`：只保存頁面標題、分類、route、canonical source 路徑與來源狀態，不保存操作手冊正文。

要加入新的 MSG／CSP 文件時，只在 `nav.json` 新增一筆 canonical `source`，並確認本機靜態伺服器能從 repository root 讀到該路徑；不要把 Markdown 正文貼進 HTML、JavaScript 或 manifest。若來源尚未確認，保留 `source: null`，讓網站顯示「來源未提供／待補」。

## 狀態與限制

頁面會顯示 `current source`、`runtime unknown` 與「來源未提供／待補」等界線。這個原型不實作登入、角色控管、資料寫入、LINE 送達驗證、部署或 production runtime 整合；畫面上可見的步驟來自執行期載入的 canonical Markdown，不能視為已部署保證。
