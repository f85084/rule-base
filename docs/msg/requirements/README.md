# MSG 需求單與文件對照

本目錄用於記錄 MSG 需求單與 RuleBase 操作文件的對應關係。

## Redmine 需求單快照

已依 Redmine 篩選條件拉取 MSG 三個專案的需求單，完整內容與摘要如下：

- [需求單摘要與清單](../../../data/sources/msg/redmine/summary_all.md)
- [完整 Redmine API 快照](../../../data/sources/msg/redmine/issues_all.json)

| Project ID | 專案 | 需求單數 |
|---:|---|---:|
| 126 | `OB_message` | 43 |
| 127 | `message-backend` | 336 |
| 128 | `message-frontend` | 153 |
| **合計** |  | **532** |

這批資料是唯讀快照，產出時間與原始查詢條件記錄在摘要檔；它只代表 Redmine 當下資料，不代表需求已完成、已驗證或已對應到 RuleBase 文件。

## 依 MSG 目錄分類

已使用 MSG B2E 實際選單作為需求分類架構，依頁面名稱與 URL 對照需求單；沒有出現在選單中的 API、JOB、Webhook、聊天室、LINE 綁定與共用技術需求，集中放到「非頁面／共用功能」。無法可靠判斷的需求則放到「待人工確認頁面」。

- [MSG 選單原始資料](../../../data/sources/msg/website-menus.json)
- [MSG 網站頁面用途索引](page-purpose-index.md)
- [MSG 需求單頁面分類 Index](page-classification-index.md)
- [MSG 需求分類證據](website-page-classification.json)
- [各頁面需求單明細](pages/)
- [MSG 業務流程對照 skill](../../../.agents/skills/msg-requirement-organization/SKILL.md)

目前分類結果：22 個 MSG 選單頁面、192 筆非頁面／共用功能、19 筆待人工確認；532 張需求單均已保留一次分類與命中依據。

98、99 另外依 `/home/art/openab-repos/project-docs/projects/MSG/data/business-flows` 補上跨頁業務流程參考；98 依流程分組，99 只列候選流程與待確認原因。重建流程可執行 `python3 scripts/enrich-msg-cross-cutting-requirements.py`。

## 後續對照欄位

建立需求對照表時，至少記錄需求單編號、專案、功能、來源文件、RuleBase 文件、狀態、測試案例與待確認事項。需求單的現況清單先以快照為準，後續再依功能群組逐批補上文件與測試追溯。
