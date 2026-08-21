# scripts/

此目錄存放一次性或輔助用的腳本。

## 主要用途

- 日常維護腳本
- 快速查詢或匯出資料的便利指令
- 開發或測試時的輔助工具

## 來源文件狀態

在對應的 `data/sources/csp/` 或 `data/sources/msg/` 放入 PDF 後執行：

```bash
python3 scripts/check-source-status.py
```

腳本會依 `data/sources/manifest.json` 的 SHA-256 判斷來源文件是「已整理」、「內容已變更，需重新整理」或「尚未整理」。檢查通過時回傳碼為 `0`；有新增或變更文件時回傳碼為 `1`，方便接到 CI 或其他自動化流程。

若要列出所有來源文件，加上 `--all`。

## MSG 需求單依網站目錄分類

先確認 `data/sources/msg/redmine/issues_all.json` 與 `data/sources/msg/website-menus.json` 已更新，再執行：

```bash
python3 scripts/classify-msg-by-website-menu.py
```

腳本會產生 `docs/msg/requirements/page-purpose-index.md`、`page-classification-index.md`、`website-page-classification.json` 與 `pages/` 下的各分類需求單清單。分類以 MSG 選單頁面／URL 為主；沒有單一前台頁面的需求放到「非頁面／共用功能」，無法判斷的需求放到「待人工確認頁面」。

完成選單分類後，若要依 MSG project-docs 業務流程補充 98/99：

```bash
python3 scripts/enrich-msg-cross-cutting-requirements.py
```

此腳本只重建 `98-非頁面-共用功能.md` 與 `99-待人工確認頁面.md`，保留 99 的人工確認狀態，並附上跨頁流程的參考來源。
