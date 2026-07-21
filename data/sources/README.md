# data/sources/

此目錄存放還未結構化的原始參考文件，作為 RuleBase 的輸入來源。

## 用途

- 暫存從 OneNote、SharePoint、PDF 等處匯出的原始文件
- 供 `tools/` 中的匯入/萃取工具處理

## 整理後的資料位置

- 測試資料整理表：`docs/test-data.md`
- 超商取貨商業規則：`docs/business-rules-pickup.md`
- 軟體電話開發、測試與錯誤碼：`docs/softphone.md`
- 音檔調聽操作：`docs/audio-recordings.md`
- 音檔索引延遲案例：`docs/audio-index-delay.md`

來源文件狀態基準：`data/sources/manifest.json`。新增或替換 PDF 後，可執行 `python3 scripts/check-source-status.py` 檢查是否需要重新整理。

## 原始文件對照

| 原始文件 | 整理文件 |
|---|---|
| `商業邏輯.pdf` | `docs/business-rules-pickup.md` |
| `軟體電話開發用.pdf`、`軟體電話測試情境.pdf`、`軟體電話相關代碼.pdf` | `docs/softphone.md` |
| `調聽音檔.pdf` | `docs/audio-recordings.md` |
| `音檔相關.pdf` | `docs/audio-index-delay.md` |

## 注意事項

- 大型 binary 檔案（如 PDF）建議視為**一次性輸入**，不適合長期留在 git 中
- 長期存放請考慮使用 git-lfs 或外部文件管理系統
