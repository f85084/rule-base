# MSG 需求單頁面分類 Index

來源需求單：`data/sources/msg/redmine/issues_all.json`
網站選單：`data/sources/msg/website-menus.json`

## 分類流程

1. 以 MSG 選單提供的頁面與 URL 作為主要分類架構。
2. 先比對需求單標題，再以標題加需求描述全文補充判斷。
3. 同一張需求單只歸入一個主要分類，保留命中位置與規則於 `website-page-classification.json`。
4. 沒有對應選單頁面的 API、JOB、Webhook、聊天室、LINE 綁定與共用技術內容，歸入「非頁面／共用功能」。
5. 無法可靠判斷時歸入「待人工確認頁面」，不自行猜測。
6. 父選單與子頁面依 JSON 的 `sort` 升冪排列；相同 `sort` 保留 JSON 原始順序，`pages/` 檔名前綴同步反映此層級。

## 分類結果

- 需求單總數：532
- MSG 目錄頁面：22
- 分類總數：24（含 MSG 目錄頁面、非頁面／共用功能與待人工確認）
- 非頁面／共用功能：192 筆
- 待人工確認頁面：19 筆

| 目錄順序 | 頁面順序 | 目錄 | 頁面 | URL | 需求單數 |
|---:|---:|---|---|---|---:|
| 1 | 1 | 權限管理 | 功能管理 | `/Function` | 0 |
| 1 | 2 | 權限管理 | 角色管理 | `/Role` | 2 |
| 1 | 3 | 權限管理 | 使用者管理 | `/User` | 15 |
| 1 | 4 | 權限管理 | 待確認使用者 | `/PendingUser` | 3 |
| 2 | 1 | 資訊報表 | 統計資訊 | `/Metrics` | 13 |
| 2 | 2 | 資訊報表 | 訊息統計資訊 | `/MessagesMetrics` | 8 |
| 2 | 3 | 資訊報表 | AI 費用報表 | `/AiCostReport` | 1 |
| 3 | 1 | 系統功能 | 離線訊息管理 | `/LeaveMessages` | 15 |
| 3 | 2 | 系統功能 | 商品維護 | `/Product` | 3 |
| 3 | 3 | 系統功能 | 模板訊息 | `/Combo` | 14 |
| 3 | 4 | 系統功能 | 遊戲管理 | `/GameManage` | 26 |
| 3 | 5 | 系統功能 | 圖庫 | `/Gallery` | 16 |
| 3 | 6 | 系統功能 | 指派 | `/Assign` | 9 |
| 3 | 7 | 系統功能 | 受眾管理 | `/Audience` | 19 |
| 3 | 8 | 系統功能 | 客戶管理 | `/Customer` | 27 |
| 3 | 9 | 系統功能 | 對話查詢 | `/Dialog` | 12 |
| 3 | 10 | 系統功能 | 客戶名單檢查 | `/CustomerCheck` | 5 |
| 3 | 11 | 系統功能 | 圖文選單 | `/Richmenu` | 11 |
| 3 | 12 | 系統功能 | 直播設定 | `/Stream` | 82 |
| 3 | 13 | 系統功能 | 簽到活動管理 | `/CheckIn` | 28 |
| 3 | 14 | 系統功能 | 照片合成功能 | `/FrameMergeActivity` | 10 |
| 4 | 1 | 系統管理 | 圖庫頁籤管理 | `/GalleryManage` | 2 |
| — | — | 共用／待確認 | 非頁面／共用功能 | `—` | 192 |
| — | — | 共用／待確認 | 待人工確認頁面 | `—` | 19 |

## 規則維護

分類規則位於 `scripts/classify-msg-by-website-menu.py`。若 MSG 目錄新增或修改頁面，先更新 `data/sources/msg/website-menus.json`，再補上規則並重新產生本索引、用途索引與 `pages/` 清單。

每一頁的需求明細位於本目錄 `pages/`；分類證據與命中原因位於 `website-page-classification.json`。

`pages/98-非頁面-共用功能.md` 與 `pages/99-待人工確認頁面.md` 另由 `scripts/enrich-msg-cross-cutting-requirements.py` 依 MSG project-docs 業務流程補上跨頁參考；這些參考不會取代選單分類，也不會把待確認需求強制歸入頁面。
