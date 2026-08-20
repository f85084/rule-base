# AI Prompt 管理

## 敘述狀態與查核界線

- **現行事實**：本頁正文依目前列出的頁面用途、操作流程與來源整理。
- **runtime 未確認**：未在目前環境實際驗證的角色按鈕、API 回應、資料同步、保存期限與版本差異，不視為目前保證；以當期 UI、API 與授權設定為準。

本篇是 CSP `/PromptManagement` AI Prompt 維護入口，供具維護權限的人員查詢、切換與儲存 Prompt 類型、Template 結構與模型設定。此頁異動的是 MariaDB Prompt 設定與其 Redis 快取，不是 `appsettings` 的 Azure OpenAI 連線設定。

## 1. 權限與資料邊界

- 登入後可載入 Prompt 維護頁；新增／修改需要 Prompt 維護權限，實際按鈕以目前帳號及環境為準。
- 頁面初始化會刻意直接查最新 Prompt，不走既有 Prompt 快取；儲存後也會清除 Prompt 快取並回傳最新清單。
- `Type` 是新增／更新的判斷鍵；不要用 Prompt 顯示名稱或前端排序取代 `Type`。
- 本頁只維護 Prompt 設定，不直接修改 Azure OpenAI endpoint、API key 或應用程式啟動設定。

## 2. 載入頁面資料

1. 開啟 `/PromptManagement`，確認目前環境與登入帳號。
2. 頁面呼叫 `GET api/PromptManagement/QueryPageInfo`，載入 Prompt 清單、Prompt 類型選項與 AI model 選項。
3. 選取要維護的 Prompt 類型，核對目前 Template、Question／參數與 ModelType；頁面會以第一筆 Prompt 作為預設顯示內容。
4. 若畫面欄位不完整，先保留原始回應與 Prompt `Type`，不要直接以空欄位覆蓋。

`QueryPageInfo` 會將儲存的 JSON Template 展開成前端可編輯結構；若有 `DefaultAnswer` 且參數中沒有 `DEFAULT_ANSWER`，回應會補入該參數。

## 3. 新增／修改 Prompt

1. 選取正確的 `Type` 與 `ModelType`，確認要編輯的是舊版 Template 或新版結構化欄位。
2. 修改 Template／Question 與參數，通過頁面欄位驗證後再儲存。
3. 儲存使用 `POST api/PromptManagement/CreateOrUpdatePrompt`；後端會先驗證 `Type`、`Template`、`ModelType`，再查詢既有 Prompt。
4. 若該 `Type` 已存在，流程走更新；不存在則新增。成功後清除 `CacheKey.AI.Prompt`，並重新查詢最新清單回傳。
5. 重新載入頁面，確認同一 `Type` 的內容、ModelType 與參數已更新；不要只以儲存按鈕沒有錯誤判斷完成。

## 維運查核補充

以下欄位、驗證、API 與快取對照只供維運查核；一般讀者先依前文完成 Prompt 類型與內容核對。

| 項目 | 規則／技術重點 |
|---|---|
| `Type` | 必填，並作為既有 Prompt 的新增／更新判斷鍵。 |
| `Template` | 必填且需能被後端處理／反序列化；格式錯誤可能造成回傳欄位無法完整展開。 |
| `ModelType` | 必填；選項由 `OpenAIModelType` 列舉提供。 |
| Prompt 類型 | 選項由 `PromptType` 列舉提供，不要自行輸入未列出的值。 |
| 參數與 `DEFAULT_ANSWER` | `DefaultAnswer` 存在但參數缺少 `DEFAULT_ANSWER` 時，初始化回應會補入。 |
| 查詢 | `GET api/PromptManagement/QueryPageInfo`；直接查最新頁面資料。 |
| 儲存 | `POST api/PromptManagement/CreateOrUpdatePrompt`；回傳儲存後最新 Prompt 清單。 |

## 5. 異常處理與排錯

| 情況 | 先檢查 | 處理方式 |
|---|---|---|
| Prompt 欄位驗證失敗 | `Type`、`Template`、`ModelType` 是否缺值或格式錯誤 | 保留畫面訊息，修正後重新送出；驗證失敗不應進入 DB 寫入。 |
| Template 展開不完整 | 原始 Template JSON、Prompt Type、參數欄位 | 不要以不完整畫面覆蓋；保存 Prompt 識別、回應與時間交由維運確認格式相容性。 |
| 儲存回報系統錯誤 | Type、帳號、請求時間與回應 | 重新載入確認是否已新增／更新；若 DB 寫入回傳 0 筆，交由系統管理員檢查。 |
| 儲存後仍看到舊 Prompt | 頁面重新查詢、Redis Prompt 快取與環境 | 先重新載入；後端成功寫入會清除 `CacheKey.AI.Prompt`，不要直接手動改快取。 |
| 修改 Azure OpenAI 設定後 AI 仍使用舊值 | 變更的是 appsettings／DI 設定還是本頁 Prompt | 本頁儲存不會重建已啟動的 AI DI service；若是應用程式設定變更，依部署流程重啟服務並驗證，不要把它當成 Prompt 儲存失敗。 |

## 6. 需求單與來源

- [AI Prompt 管理需求](<../requirements/pages/53-AI Prompt 管理.md>)：1 筆需求單，頁面路由 `/PromptManagement`。
- 需求單：[#46568 Prompt 設定頁面](../../../data/sources/csp/redmine/issues_all.json)。
- [MI 完整手冊](MI完整手冊.md)、[網站選單來源](../../../data/sources/csp/website-menus.json)、[Redmine 來源快照](../../../data/sources/csp/redmine/issues_all.json)。
