# Rules

此目錄存放 RuleBase 的規則與領域知識結構，包含：

- 領域實體（DomainEntity）定義
- 商業規則（BusinessRule）的結構化描述
- 文件片段（DocumentChunk）與向量索引設定
- 規則執行引擎可讀取的 JSON / DSL 格式

初期預計使用 PostgreSQL + pgvector 作為底層儲存，讓結構化規則與語意向量能統一管理。
