# RuleBase 架構（現行簡化版）

> 本文件描述 RuleBase **目前實際採用**的架構。若需與原始規劃比對，請參考 `ARCHITECTURE.md`。

## 現階段目標

RuleBase 目前作為**統一測試資料與規則參考知識庫**，優先解決「測試資料散落各處、難以查詢」的問題。

不強求機器可讀的規則引擎或結構化資料庫，而是先以**人類可讀、AI 可檢索**的 Markdown 文件為核心。

## 高階架構

```
使用者 / AI bot
    │
    ├── 查詢測試資料 → docs/csp/test-data/test-data.md
    ├── 查詢原始文件 → data/sources/csp/
    └── 未來擴充 → data/rules/、data/samples/、engine/、tools/
```

## 目錄對應（現行）

| 目錄 | 用途 |
|---|---|
| `docs/` | 設計文件與測試資料參考表 |
| `docs/architecture/ARCHITECTURE.md` | 原始完整架構規劃（規則引擎、RAG、資料庫） |
| `docs/architecture/ARCHITECTURE-current.md` | 本文件，描述目前簡化架構 |
| `docs/csp/test-data/test-data.md` | 主要測試資料整理表，供人員與 bot 查詢 |
| `data/rules/` | 未來放置結構化規則與領域知識，目前為預留目錄 |
| `data/samples/` | 未來放置結構化測試資料樣本，目前為預留目錄 |
| `data/sources/csp/` | CSP 原始參考文件（PDF、OneNote 匯出檔等輸入來源） |
| `engine/` | 未來規則執行引擎程式碼，目前為預留目錄 |
| `tools/` | 未來資料匯入、同步、驗證工具，目前為預留目錄 |
| `scripts/` | 未來一次性或輔助腳本，目前為預留目錄 |

## 核心資料流

1. **原始文件匯入**：從 OneNote、SharePoint、PDF 等處取得 CSP 原始文件，放入 `data/sources/csp/`。
2. **人工整理**：將原始文件中的測試資料、注意事項整理成 Markdown 表格，放入 `docs/csp/test-data/test-data.md`。
3. **查詢使用**：開發者、測試人員或 AI bot 直接閱讀 `docs/csp/test-data/test-data.md` 取得測試所需資訊。

## 技術選型（現行）

- **儲存格式**：Markdown（.md）
- **檢索方式**：文字搜尋 / 未來可導入 RAG 向量檢索
- **版本控制**：Git
- **協作方式**：直接編輯 Markdown 文件

## 未來可擴充方向

當測試資料與規則數量增加、需要機器自動判斷時，再逐步引入：

1. 結構化 schema 與商業規則（`data/rules/`）
2. 規則執行引擎（`engine/`）
3. 資料匯入與驗證工具（`tools/`）
4. 結構化資料庫（PostgreSQL）與向量資料庫（pgvector）

## 與原始規劃的差異

| 項目 | 原始規劃（ARCHITECTURE.md） | 現行簡化版 |
|---|---|---|
| 核心格式 | YAML/JSON + 自訂 DSL | Markdown 表格 |
| 規則引擎 | Rules Evaluator | 尚未實作 |
| 資料庫 | PostgreSQL + pgvector | 無，以 Git + Markdown 管理 |
| RAG | 向量資料庫檢索 | 未來可導入，目前靠文字搜尋 |
| 資料來源 | business-flows、原始碼、fixtures、專家知識 | 目前先整理現有測試資料 PDF |
