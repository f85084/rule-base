# scripts/

此目錄存放一次性或輔助用的腳本。

## 主要用途

- 日常維護腳本
- 快速查詢或匯出資料的便利指令
- 開發或測試時的輔助工具

## 來源文件狀態

在 `data/sources/` 放入 PDF 後執行：

```bash
python3 scripts/check-source-status.py
```

腳本會依 `data/sources/manifest.json` 的 SHA-256 判斷來源文件是「已整理」、「內容已變更，需重新整理」或「尚未整理」。檢查通過時回傳碼為 `0`；有新增或變更文件時回傳碼為 `1`，方便接到 CI 或其他自動化流程。

若要列出所有來源文件，加上 `--all`。
