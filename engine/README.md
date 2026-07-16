# engine/

此目錄存放 RuleBase 的規則執行引擎（Rules Evaluator）。

負責讀取 `data/rules/` 中的規則定義，並將其轉換為可執行的判斷邏輯。

## 主要用途

- 解析規則定義檔（YAML/JSON DSL）
- 執行規則判斷並回傳結果
- 提供規則執行的 API 或 CLI 介面

## 與 data/rules/ 的關係

- `data/rules/`：規則的**靜態定義**
- `engine/`：執行規則的**程式碼**
