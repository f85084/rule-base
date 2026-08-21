# 需求單依網站頁面整理流程

這份流程用於 CSP、MSG 等專案，將需求單依實際網站頁面與 URL 整理，並保留可追溯的來源與分類依據。

## 目前 CSP 實際執行過的流程

### 1. 確認工作專案與來源

- 確認目前專案目錄，例如 `/home/art/openab-repos/rule-base`。
- 確認需求單原始 JSON 的位置。
- 原始 JSON 只讀取、不直接修改，作為後續驗證基準。

### 2. 取得實際網站選單

- 以網站提供的選單資料為準，不自行建立抽象的功能大類。
- 保存頁面名稱與 URL，例如：`訂單管理` → `/OrderHistory`。
- 選單資料保存於 `data/sources/<project>/website-menus.json`。

### 3. 對照既有專案文件

- 從 `project-docs` 的 L2 頁面索引與「頁面全貌」文件取得頁面用途。
- 依 URL 對照頁面，不只依頁面名稱比對；需處理大小寫、反引號與是否有 `/` 的差異。
- 產生頁面用途索引，記錄：頁面名稱、URL、用途摘要、來源文件。
- 找不到來源文件的頁面保留在索引中，標記為待補，不自行猜測。

目前使用的工具：

```text
scripts/generate-page-purpose-index.py
docs/csp/requirements/page-purpose-index.md
```

### 4. 建立分類規則

- 分類規則以網站實際頁面／URL 為單位。
- 具體頁面規則放在前面，共用功能規則放在後面。
- 先比對需求單標題，再用標題加描述補充判斷。
- 每張需求單只歸入一個主要頁面，避免同一筆需求重複出現在多個分類。
- API、背景排程、資料庫、登入、Session、共用元件、全站樣式等沒有單一頁面的內容，歸入「非頁面／共用功能」。
- 無法可靠判斷時，先放入「待人工確認頁面」，不要只因單一關鍵字命中就強行分類。

目前 CSP 使用：

```text
scripts/classify-redmine-by-website-page.py
docs/csp/requirements/page-classification-index.md
docs/csp/requirements/pages/
docs/csp/requirements/website-page-classification.json
```

### 5. 產生頁面需求清單

每個頁面產生一份 Markdown 清單，至少保留：

- Redmine 需求單連結與編號
- 標題
- 類型
- 狀態
- 負責人
- 建立日期
- 頁面 URL

### 6. 完整性驗證

重新整理後必須確認：

- 分類總數等於原始需求單總數。
- 每筆需求單只出現一次。
- 沒有遺漏需求單。
- 網站選單中的頁面，即使目前是 0 筆，也要能被辨識。
- 原始 JSON 未被修改。
- 產生的文件沒有殘留上一輪已刪除或改名的分類檔案。

### 7. 文件入口保持單純

- 頁面用途索引負責說明「這個 URL 頁面做什麼」。
- `page-classification-index.md` 負責說明「需求單如何判斷歸類」。
- `pages/` 負責保存各頁面的需求單明細。
- 不再另外維護與上述內容重複的總需求分類索引。

## MSG 實際套用流程

1. 先取得 MSG 三個專案的原始需求單資料，保存於 `data/sources/msg/redmine/issues_all.json`。
2. 將 MSG 實際網站選單 API 回應保存於 `data/sources/msg/website-menus.json`。
3. 讀取 `project-docs` 中 MSG 對應的 B2E L2 頁面文件，產生 `docs/msg/requirements/page-purpose-index.md`。
4. 執行 `scripts/classify-msg-by-website-menu.py`，依頁面用途、URL、標題與描述產生分類。
5. 產生 `docs/msg/requirements/pages/` 下的每頁需求清單與 `website-page-classification.json` 命中依據。
6. 做總數、唯一性、遺漏、選單頁面完整性與原始來源未修改等驗證。
7. 將結果與待人工確認項目寫入 `docs/msg/requirements/README.md`。

## 重要原則

- 網站頁面／URL 是主要分類架構，功能群組只作為網站選單中的上層資訊。
- 頁面用途是分類判斷依據；關鍵字只是輔助，不應凌駕頁面用途。
- 跨頁面或整個系統的需求放到「非頁面／共用功能」。
- 每次產生或刪除文件後，都要同步更新 README 與工作摘要。
