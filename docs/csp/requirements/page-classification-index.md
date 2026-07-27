# CSP 需求單頁面分類 Index

來源需求單：`data/sources/csp/redmine/issues_all.json`
網站選單：`data/sources/csp/website-menus.json`

## 分類流程

1. 先讀取需求單標題，依下方規則的優先順序判斷。
2. 標題沒有命中時，再用標題加需求描述全文判斷。
3. 同一張需求單只歸入第一個命中的主要頁面。
4. 沒有命中時才會進入「待人工確認頁面」；API、背景作業、共用元件與全站功能歸入「非頁面／共用功能」。
5. 規則順序由具體頁面到共用功能；後面的規則不會覆蓋前面已命中的頁面。

## 分類規則（依優先順序）

| 順序 | 頁面 | URL | 判斷關鍵字／模式 |
|---:|---|---|---|
| 1 | 系統功能 | `/Function` | `系統功能 · 功能權限` |
| 2 | 系統角色 | `/Role` | `系統角色 · 角色管理 · 角色功能 · 角色權限 · 角色設定` |
| 3 | 帳號設定 | `/User` | `帳號設定 · 帳號管理 · 使用者帳號 · AD帳號 · 帳號鎖定` |
| 4 | TM名單推薦 | `/OutBoundTmList` | `TM名單 · TM推薦 · 人物誌 · 人物摘要 · 360畫像 · 360標籤 · 標籤評價 · 點讚 · 推薦名單 · 客戶分群 · 分群推薦` |
| 5 | 客戶查詢 | `/CustomerService` | `客戶查詢 · 客服查詢 · CustomerService` |
| 6 | 接單作業 | `/Order` | `接單作業 · 接單 · 訂購 · 下單 · 商品查詢` |
| 7 | 銷退管理 | `/Return` | `銷退 · 退貨 · 換貨 · 拒收 · 退回` |
| 8 | 訂單管理 | `/OrderHistory` | `訂單管理 · 訂單 · 配送 · 發票 · 載具 · 訂閱制 · 付款 · 信用卡 · 購物車 · 商品 · 分期 · 零卡 · ATM匯款 · 購樂趣 · 結帳區 · 快速到貨 · 超取 · 宅家取 · 折價券 · 退款帳號` |
| 9 | 客訴處理 | `/CustomerComplaint` | `客訴 · 抱怨 · CustomerComplaint` |
| 10 | 會員明細 | `/Customer` | `會員明細 · 會員資料 · 會員 · 客戶資料 · 大健康 · 切換客戶 · 切換指定客戶 · 新增地址 · Customer(?!Service) · ContactId · 手機資料` |
| 11 | 帳戶明細 | `/DiscountTransaction` | `帳戶明細 · 帳戶交易 · 現金帳戶 · 藍鑽 · 點數 · E幣 · 貴賓券` |
| 12 | 聯繫歷史 | `/ContactHistory` | `聯繫歷史 · 聯絡記錄 · 交談記錄 · 互動記錄 · 訊息歷史` |
| 13 | 電話小結作業 | `/CallSummary` | `電話小結 · 通話小結 · 小結作業 · 小結內容 · 小結欄位` |
| 14 | 客服員待辦事項 | `/OutBoundTodoList` | `客服員待辦 · 待辦事項 · 客服待辦` |
| 15 | 問卷管理 | `/Survey` | `問卷 · 問券 · Survey · 第一題` |
| 16 | 活動管理 | `/Activity` | `活動管理 · 活動設定 · 東森樂透 · 小額奪寶 · 活動報名 · 限量品 · 樂透 · 行銷活動` |
| 17 | 票劵/預約 | `/NaturalBeauty` | `票券 · 票劵 · 預約 · 自然美` |
| 18 | 直播/見面會報名 | `/LiveStreamSignUp` | `直播報名 · 見面會報名 · 直播/見面會報名 · 報名介面 · 報名明細 · 歷史報名` |
| 19 | 商品訊息 | `/SaleMessage` | `商品訊息 · 商品話術 · 銷售話術` |
| 20 | 訊息查詢 | `/Message` | `訊息查詢 · 傳送訊息 · 訊息紀錄 · 即時訊息 · 歷史訊息 · 發送訊息 · 訊息轉發 · 簡訊 · Message · LINE` |
| 21 | 通知中心 | `/Notifications` | `通知中心 · 通知 · 提醒 · 推播` |
| 22 | 調聽音檔 | `/AudioLog` | `調聽音檔 · 音檔管理 · 調聽撥放 · 調聽播放器 · 音檔播放器 · 音檔位置 · 錄音 · 播放清單 · 撥放清單 · connection.?id · ConnId · SIP.?Record` |
| 23 | 優質音檔 | `/AudioShared` | `優質音檔 · 優良音檔 · 分享音檔 · 話術音檔` |
| 24 | 訂單質檢 | `/OrderQA` | `訂單質檢 · 質檢單 · 質檢流程 · 質檢批次 · 質檢類型 · 質檢匯入 · 質檢Excel · 質檢累犯 · 質檢歷程 · 質檢主檔 · 查核質檢 · 組長質檢 · 質檢的音檔 · 新增質檢 · 獎勵質檢 · 大批質檢 · 自首件 · OrderQA` |
| 25 | 質檢查核 | `/OrderQACheck` | `質檢查核 · 質檢審核 · 複審 · OrderQACheck` |
| 26 | 質檢查詢 | `/OrderQAQuery` | `質檢查詢 · 質檢報表 · 質檢匯出 · OrderQAQuery` |
| 27 | 質檢項目維護 | `/OrderQAStandard` | `質檢項目 · 質檢標準 · OrderQAStandard` |
| 28 | 客戶進階查詢 | `/SuperiorQuery` | `客戶進階查詢 · 進階查詢 · SuperiorQuery` |
| 29 | 客服即時狀態 | `/OutBoundStatus` | `客服即時狀態 · 即時客服狀態 · 線上狀態` |
| 30 | 客服文件管理 | `/Document` | `客服文件 · 文件管理 · 讀取文件 · 下載文件 · Document(?!QA)` |
| 31 | 使用者設定 | `/Agent` | `代理人設定 · 職務代理人 · 代理清單 · 代理人 · 使用者設定` |
| 32 | 審核作業 | `/Review` | `審核作業 · 審核功能 · 審核清單 · 待審資料 · Review` |
| 33 | 跑馬燈管理 | `/Marquee` | `跑馬燈` |
| 34 | 公告管理 | `/Announcement` | `公告管理 · 公告` |
| 35 | 組織部門設定 | `/Department` | `部門 · 組織 · 組織階層` |
| 36 | 直播/見面會管理 | `/LiveStreamManage` | `直播/見面會管理 · 直播管理 · 見面會管理 · 直播/見面會活動類型` |
| 37 | 行事曆管理 | `/Meeting` | `行事曆管理 · 管理行事曆 · 工作日 · Meeting` |
| 38 | 行事曆 | `/Calendar` | `行事曆 · 課程 · 記事本` |
| 39 | 商品加量管理 | `/ProductIncrease` | `商品加量 · 加量管理` |
| 40 | 外呼組別管理 | `/OutBoundTeam` | `外呼組別 · 組別成員` |
| 41 | 名單歷程查詢 | `/OutBoundCustomer` | `名單歷程 · 名單查詢 · 名單記錄 · 名單轉換` |
| 42 | 名單轉派申請 | `/OutBoundListTransferApply` | `轉派申請 · 申請轉派` |
| 43 | 名單轉派審核 | `/OutBoundListTransferReview` | `轉派審核 · 審核轉派` |
| 44 | 名單轉派查詢 | `/OutBoundListTransfer` | `名單轉派 · 轉派功能 · 轉派查詢 · 轉派歷程 · 轉派退件` |
| 45 | 名單小組管理 | `/OutBoundListManagement` | `名單小組 · 沉澱會員 · 名單回收` |
| 46 | 小結清單 | `/ContactSummary` | `小結清單 · 小結狀態 · 小結查詢` |
| 47 | 撥號日期管理 | `/DialScheduler` | `撥號日期 · 前置碼 · DialScheduler` |
| 48 | Domain管理 | `/DomainData` | `Domain管理 · DomainData` |
| 49 | 排程工作狀態 | `/JobStatus` | `排程工作 · JOB狀態 · JobStatus` |
| 50 | 工作日管理 | `/WorkingDay` | `工作日管理 · 政府機關行事曆` |
| 51 | 外部服務呼叫紀錄 | `/ApiLog` | `外部服務 · API Log · ApiLog · 呼叫紀錄` |
| 52 | AI Prompt 管理 | `/PromptManagement` | `Prompt設定 · Prompt管理 · 提示詞設定` |
| 53 | AI 費用報表 | `/AiCostReport` | `AI費用 · AI 成本 · 費用報表` |
| 54 | 小m文件管理 | `/DocumentQA` | `小M文件 · 小m文件 · 文件給 AI · Qdrant` |
| 55 | 小m使用紀錄 | `/DocumentQARecord` | `小M使用 · 小m使用 · 問答紀錄 · AI使用紀錄` |
| 56 | 郵件通知紀錄 | `/MailNotice` | `郵件通知 · MailNotice · Mail` |
| 57 | 非頁面／共用功能 | `—` | `軟體電話 · CTI · SIP · API · JOB · 排程 · Redis · 資料庫 · DB · SP · SQL · sonarqube · 原碼 · 架構 · 效能 · 快取 · SSO · 微服務 · 登入 · login · 登出 · Session · Token · AntiForgery · HttpClient · traceId · 全站 · 首頁 · 前端 · ESM · Layout · header · Cache-Control · cache · webpack · Bundle · bundle · css · scss · sass · Style · 樣式 · 字體 · font · 選單 · 左側 · LightboxModal · 500畫面 · Log · LOG · 爬蟲 · MCP · Framework · framework · 升版 · Exception · exception · 錯誤 · 環境 · int溢位 · 儀表板 · MI Search · 圖檔存取 · 圖片剪裁 · 上傳圖片 · 我的最愛 · modalHelper · 字串轉換 · 暗系列 · 暗色系 · AgentID · 時間格式 · AI · 小M · 小m · 對話紀錄 · 問答 · Tag · streaming · POC · 驗證 · 功能優化 · TempData · ajax · 網頁 · 移除不必要 · 移除.*程式 · 地址元件 · 使用者物件 · 個人存放區 · 提示訊息 · 撈取專員使用 · 外撥 · 進線 · 通話中 · 頁面` |

## 分類結果

- 需求單總數：1555
- 分類總數：58（含網站頁面、非頁面／共用功能與待人工確認）
- 非頁面／共用功能：219 筆
- 待人工確認頁面：0 筆
- 每筆分類的實際命中依據另記錄於 `website-page-classification.json` 的 `evidence`。

## 維護方式

若網站新增或修改頁面，先更新 `data/sources/csp/website-menus.json`，再在本腳本的 `RULES` 補上頁面關鍵字，最後重新執行分類腳本。
