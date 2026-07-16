# Rules

此目錄存放 RuleBase 的規則與領域知識結構，包含：

- `schemas/`：資料實體的 YAML schema（欄位、型別、範例）
- `entities/`：領域實體（DomainEntity）定義，說明每個實體的業務意義
- `business-rules/`：商業規則（BusinessRule）的結構化描述，供規則引擎執行
- 未來可加入 `document-chunks/`：文件片段（DocumentChunk）與向量索引設定

初期預計使用 PostgreSQL + pgvector 作為底層儲存，讓結構化規則與語意向量能統一管理。
