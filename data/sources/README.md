# data/sources/

此目錄存放尚未結構化的原始參考文件，並依專案分開保存。

## 專案目錄

- `csp/`：CSP 原始文件
- `msg/`：MSG 原始文件

整理後的文件總索引：`docs/README.md`

來源文件狀態基準：`data/sources/manifest.json`。新增或替換 PDF 後，可執行：

```bash
python3 scripts/check-source-status.py
```

## 注意事項

- 原始 PDF 可能包含帳號、密碼、Token、手機號碼與其他內部資料。
- 敏感資料不應複製到一般 Markdown、提示詞或圖片。
- 大型 binary 檔案建議視為一次性輸入；長期存放請考慮 git-lfs 或外部文件管理系統。
