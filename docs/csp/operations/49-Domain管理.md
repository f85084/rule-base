# Domain管理

本頁對應 `/DomainData` 的系統設定入口。Domain Schema 定義欄位的 `Key`、型別與限制，Domain Data 則把實際值組成 JSON 儲存；兩者不是一般業務頁面的查詢條件。此頁在需求盤點中為 0 筆需求單，內容僅依 [Domain管理需求頁](../requirements/pages/49-Domain管理.md)、選單與既有操作來源整理。

## 入口與權限

- 網站路由：`/DomainData`；可由 [website-menus.json](../../../data/sources/csp/website-menus.json) 的 `id: 53` 核對，選單分類為「系統管理」。
- 查詢 API 是登入後查詢範圍；建立 Schema、建立／更新 Data、切換啟用與刪除屬於維護操作，應具相應功能權限。實際按鈕顯示與 API 授權以登入帳號角色為準。
- 這是通用動態設定頁，不能因為某個 Domain 名稱出現在其他流程，就推定本頁知道其業務意義或可任意修改。

## 查詢與維護流程

| 操作 | API 路由 | 流程與結果 |
|---|---|---|
| 載入完整模型 | `GET api/DomainData/QueryDomainModel` | 同時讀 Schema、Data；快取命中則使用 Redis，否則查 MariaDB，再將 `Value` JSON 反序列化，依 Domain／`Sort` 組裝排序。 |
| 型別下拉 | `GET api/DomainData/QueryDropDownList` | 由 Schema type enum／reflection 組出，不查 DB。 |
| 建立 Schema | `POST api/DomainData/CreateDomainSchema` | 同一 Domain 不可重複；一組 Schema 批次寫入 `usp_domain_schema_add`，成功清除 Schema／Data 快取。 |
| 新增 Data 表單 | `GET api/DomainData/QueryDomainDataModel?domain={domain}` | 依既有資料及 Schema 組出預設模型；無既有資料時 DomainId 從 `1001` 開始。 |
| 新增 Data | `POST api/DomainData/CreateDomainData` | 依 Schema 補上欄位型別／Limit，建立者取登入者，組成 JObject 後寫入 `usp_domain_data_add`。 |
| 更新 Data | `POST api/DomainData/UpdateDomainData` | 依 Schema 驗證後序列化，修改者取登入者，寫入 `usp_domain_data_update`。此流程會強制 `Enable=true`。 |
| 啟用／停用 | `GET api/DomainData/UpdateDomainDataEnable?id={id}` | 依 ID 反轉 `Enable`；查無資料回 `false` 與「找不到指定的 DomainData」。 |
| 刪除 Domain | `GET api/DomainData/DeleteDomain?domain={domain}` | 以 Domain 為邊界刪除其 Schema 與 Data，並清除兩組快取；不是單筆資料的隱藏刪除。 |

## 欄位、驗證與狀態

- Schema 的核心欄位是 Domain、`Key`、Type、Limit。Domain 不可重複；`Key` 受 validator 限制為英文字母；`Limit` 必須是正整數。
- Data 以 Schema 定義的欄位值送出。新增／更新會逐欄位檢查字串、數字與長度限制；Schema 對不上、型別不符或無法序列化為 JSON 時，不進入成功寫入。
- Data 狀態由 `Enable` 表示。更新資料與單獨切換狀態共用 update SP；尤其更新內容時會把 `Enable` 送成 true，若目的是停用，應使用 `UpdateDomainDataEnable` 後重新查詢確認。
- DomainId 是每個 Domain 內的遞增識別值，不是跨 Domain 的全域流水號；新增空 Domain 時從 `1001` 起算。

## 資料邊界、例外與排錯

- MariaDB：`usp_domain_schema_getall`、`usp_domain_data_getall`、`usp_domain_schema_add`、`usp_domain_data_add`、`usp_domain_data_update`、`usp_domain_data_delete`；Redis 快取鍵為 `DomainManagement_DomainSchema` 與 `DomainManagement_DomainData`。所有寫入成功後都應清除相應快取。
- `QueryDomainModel` 遇到非法 JSON 會在反序列化時失敗；新增失敗可能回 `SystemError: 新增失敗`；刪除底層失敗會包成 `InvalidArgument` 並保留原始訊息。
- 建立 Schema 若遇到同名 Domain，回「儲存失敗，已有相同Domain」；啟用／停用查無 ID 則是失敗回應，不是新增資料。
- log-map 沒有 NormalLogger 特徵。排錯至少保留 Domain、Data ID、操作 API、登入者、時間、回應訊息與 trace/tid；先分辨 DB 寫入成功但 Redis 尚未更新，或是 Schema／JSON validator 在前端送出前已拒絕。
- 本頁沒有需求單，不應把其他 Domain 的參數、業務狀態或下游快取 TTL 當成本頁固定規格。完整背景可參考 [MI完整手冊](MI完整手冊.md)。

## 相關入口

- [Domain管理需求](../requirements/pages/49-Domain管理.md)
- [系統角色](02-系統角色.md)、[系統功能](01-系統功能.md)
