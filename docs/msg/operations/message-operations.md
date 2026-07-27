# 訊息系統操作與設定

來源：

- `data/sources/msg/OB Message 筆記本.pdf`
- `data/sources/msg/LIFF 頁設定.pdf`
- `data/sources/msg/Wiki_APM其他設定.pdf`
- `data/sources/msg/所有環境.pdf`

## 相關環境

訊息系統依環境分為正式區、Stage、Test 與 Lab，詳見 [MSG 環境資訊](../test-data/test-data-environments.md)。

## LIFF 設定

原始文件包含 LIFF 頁面、Channel ID 與本機設定範例。這些設定會依專案與環境不同，實際使用時應以目前的環境設定或密鑰管理系統為準；本文件不複製完整 ID、Token、個人資料或 SQL 初始化資料。

## 測試綁定流程注意事項

- 綁定當下才會寫入客代；若當下查不到富購帳號，之後補上資料不會自動回填。
- 若綁定當下沒有維運專員，之後補掛專員也不會自動回填客代。
- 排查綁定問題時，依原始文件確認 `clients`、`client_user`、`client_user_log` 與 `chatrooms` 的關聯狀態。
- 清除測試資料前，先確認客戶 ID、環境與影響範圍，避免誤動正式資料。

## APM／ELK 查詢

`Wiki_APM其他設定.pdf` 提供訊息資料匯入 ELK 的 SQL 範例，欄位包含聊天室、客代、訊息、說話者、建立／更新時間與專員資訊。查詢時應遮罩手機等個資，並依目前資料庫結構與權限調整；不直接把完整查詢或排除清單複製到此文件。

## 敏感資料

原始 PDF 含有環境 URL、帳號、密碼、Channel 設定、手機號碼與客戶資料。這些內容只保留在受控的原始文件或密鑰管理位置，不應貼入 Markdown、提示詞或圖片。
