# CSP 需求單與文件對照

本目錄用於記錄 CSP 需求單與 RuleBase 操作文件的對應關係。

完整業務流程與技術文件來源：

```text
/home/art/openab-repos/project-docs/projects/CSP/data/business-flows/
```

建立對照表時，至少記錄需求單編號、功能、來源文件、RuleBase 文件與待確認事項。

## 目前整理結果

- [CSP 整理進度表](progress.md)
- [頁面分類 Index（判斷順序與關鍵字）](page-classification-index.md)
- [頁面用途索引（來源：project-docs）](page-purpose-index.md)
- [網站頁面分類結果與命中依據](website-page-classification.json)
- [需求單對應的操作文件缺口](missing-operation-pages.md)
- [網站選單來源](../../../data/sources/csp/website-menus.json)

分類文件以使用者提供的網站選單為基準，需求單標題優先、描述補充；每張需求單先歸入一個主要頁面，並保留原始需求單編號與狀態。

## 整理狀態

- `page-purpose-index.md` 的泛用用途摘要已依對應 L1／L2 與操作文件補強；`郵件通知紀錄` 保留目前只有選單、route 與 0 issue 可確認的來源邊界。
- 後續若來源快照或網站選單變更，需同步校正頁面用途、route、分類規則與各操作入口。
