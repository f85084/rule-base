# MSG 業務流程對照路由

這份路由只用來整理 `98-非頁面-共用功能.md` 與 `99-待人工確認頁面.md`。
它不會改變 `scripts/classify-msg-by-website-menu.py` 對 MSG 選單頁面的正式分類。

## 對照群組

| 群組 | 主要訊號 | 主要參考來源 |
|---|---|---|
| LINE Webhook 與客戶生命週期 | Webhook、follow、unfollow、postback、Line SDK、Profile、Channel | `data/business-flows/special/MSG-LINE-Webhook客戶生命週期.md`、`data/business-flows/WebAPI/L1/WebHook.md` |
| LINE／LIFF 身分綁定與客戶身分 | LIFF、綁定、客代、手機驗證、OTP、電話驗證 | `data/business-flows/special/MSG-LIFF手機驗證與客代綁定.md`、`data/business-flows/special/MSG-B2C-LIFF身分驗證.md` |
| B2E 即時客服對話、訊息與派線 | 聊天室、訊息、離線、SignalR、未讀、派線、指派、封鎖 | `data/business-flows/B2E/L3/即時客服對話與派線流程.md`、`data/business-flows/special/MSG-訊息保存即時通知與離線回覆.md` |
| B2E 行銷群發與內容素材 | 群發、模板、商品、圖庫、圖文選單、素材、推播 | `data/business-flows/B2E/L3/行銷群發與內容素材管理.md`、`data/business-flows/B2E/L1/Multi.md` |
| B2E 受眾、客戶與標籤 | 受眾、分眾、標籤、客戶名單、會員、客戶狀態 | `data/business-flows/B2E/L3/受眾分群與標籤管理.md`、`data/business-flows/B2E/L1/Audience.md` |
| B2E 互動行銷、簽到與遊戲 | 活動、簽到、報到、遊戲、抽獎、照片合成、拍照活動 | `data/business-flows/B2E/L3/互動行銷與簽到遊戲管理.md`、`data/business-flows/B2E/L1/CheckIn.md` |
| B2E 直播、統計與 AI | 直播、統計、報表、AI、摘要、費用、ELK、GA/GTM | `data/business-flows/B2E/L3/直播、統計與費用監控.md`、`data/business-flows/B2E/L1/Metrics.md` |
| B2E 登入、帳號與權限 | 登入、帳號、使用者、角色、權限、SSO、MI、LDAP/AD | `data/business-flows/B2E/L3/登入與安全權限治理.md`、`data/business-flows/special/MSG-MI-SSO自動建立帳號機制.md` |
| 共用技術、資料與維運 | 架構、資料表、套件、環境、排程、Redis、SonarQube、共用元件 | `data/business-flows/INDEX.md`、`data/business-flows/B2E/L1/INDEX.md` |

## 判斷順序

1. 先用需求標題比對群組，再用描述補充；避免描述裡的程式碼名稱
   覆蓋標題已表達的業務意圖。
2. Webhook、聊天室、LIFF 綁定等跨頁技術鏈路，保留在 98，不轉成某個
   前台頁面。
3. 99 的群組名稱是候選，不是正式歸類。沒有足夠上下文時使用「共用
   技術、資料與維運」並明確寫出「尚無可靠候選」。
4. 若人工確認後能對應 MSG 選單頁面，應修改正式分類器規則並重新產生
   全部索引；不要只手改 99 的單列。

## 變更來源

當 MSG 選單、L3 業務流程或 L1 文件新增／改名時，先確認來源檔案的實際
路徑，再同步更新 `scripts/enrich-msg-cross-cutting-requirements.py` 與本
路由表。產出文件應保留來源文件名稱，方便測試人員和不熟系統的人追查。
