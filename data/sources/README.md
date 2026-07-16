# data/sources/

此目錄存放還未結構化的原始參考文件，作為 RuleBase 的輸入來源。

## 用途

- 暫存從 OneNote、SharePoint、PDF 等處匯出的原始文件
- 供 `tools/` 中的匯入/萃取工具處理

## 整理後的資料位置

- 測試資料整理表：`docs/test-data.md`

## 注意事項

- 大型 binary 檔案（如 PDF）建議視為**一次性輸入**，不適合長期留在 git 中
- 長期存放請考慮使用 git-lfs 或外部文件管理系統
