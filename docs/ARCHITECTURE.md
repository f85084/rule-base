# RuleBase 架構

## 高階架構

```
應用層 (AI / 開發者 / 測試工具)
    │
    ├── RAG 問答
    ├── 規則執行
    └── 測試資料查詢
    │
知識組織層 (RuleBase 核心)
    │
    ├── DomainEntity        # 領域實體
    ├── BusinessRule        # 商業規則
    ├── TestCase            # 測試案例
    ├── TestData            # 測試資料
    ├── DocumentChunk       # 文件片段
    └── Tag / Version       # 標籤與版本
    │
資料層
    ├── 結構化資料庫 (PostgreSQL)
    ├── 向量資料庫 (pgvector / Chroma / Milvus)
    └── 規則執行引擎 (Rules Evaluator)
```

## 目錄對應

- `data/rules/`：DomainEntity / BusinessRule / DocumentChunk 的結構化定義
- `data/samples/`：TestCase / TestData 的範例資料

## 核心概念

| 實體 | 說明 |
|------|------|
| DomainEntity | 業務領域實體，例如「客服工單」「客訴分類」「客服人員」 |
| BusinessRule | 綁定 DomainEntity 的商業規則，以結構化 DSL 描述 |
| TestCase | 對應一或多條 BusinessRule 的測試案例 |
| TestData | TestCase 的輸入與預期輸出 |
| DocumentChunk | 原始文件片段，綁定 DomainEntity / BusinessRule，用於 RAG |

## 資料來源

1. `project-docs/projects/CSP/data/business-flows`（L1/L2/L3/special）
2. 原始碼 Repository
3. 現有測試資料與 fixtures
4. 領域專家知識

## 技術選型（待確認）

- 結構化資料庫：PostgreSQL（建議搭配 pgvector）
- 向量資料庫：pgvector（簡化部署）或獨立 Chroma / Milvus
- 規則引擎：自訂 JSON DSL + 解釋器
- 同步腳本：Node.js / Python（視專案技術棧而定）
