# MSG 環境資訊

來源：

- `data/sources/msg/Lab資訊.pdf`
- `data/sources/msg/Test 資訊.pdf`
- `data/sources/msg/Stage 資訊.pdf`
- `data/sources/msg/所有環境.pdf`
- `data/sources/msg/(原PHP)B區line@原PHP架構Lab資料.pdf`
- `data/sources/msg/OB Message 筆記本.pdf`

## 環境位址

先依「使用環境」尋找入口，再依入口類型選擇 B2E、B2C API 或 Web：

```text
MSG 環境
├─ Lab       測試開發
│  ├─ B2E
│  ├─ B2C API
│  └─ Msg@ Web
├─ Test      測試／驗證
│  ├─ B2E
│  ├─ B2C API
│  └─ Web
├─ Stage     預發布
│  ├─ B2E
│  └─ B2C API
└─ 正式區     正式服務
   └─ B2E
```

### Lab｜測試開發

| 入口 | 位址 | 用途 |
|---|---|---|
| B2E | [開啟 Lab B2E](https://im-lab.etzone.net/) | 測試開發環境 |
| B2C API | [開啟 Lab B2C API](https://imapi-lab.etzone.net/) | 測試開發 API |
| Msg@ Web | [開啟 Lab Msg@ Web](https://im-web-lab.etzone.net/) | 訊息系統前端 |

### Test｜測試／驗證

| 入口 | 位址 | 用途 |
|---|---|---|
| B2E | [開啟 Test B2E](https://msg-test.etzone.net/) | AD 登入 |
| B2C API | [開啟 Test B2C API](https://msgapi-test.etzone.net/) | 測試 API |
| Web | [開啟 Test Web](https://msg-web-test.etzone.net/) | 測試前端 |

### Stage｜預發布

| 入口 | 位址 | 用途 |
|---|---|---|
| B2E | [開啟 Stage B2E](https://msg-stage.ehsn.com.tw/) | Stage 環境 |
| B2C API | [開啟 Stage B2C API](https://msg-stage-api.ehsn.com.tw/) | Stage API |

### 正式區｜正式服務

| 入口 | 位址 | 用途 |
|---|---|---|
| B2E | [開啟正式區 B2E](https://msg.ehsn.com.tw/) | 正式環境 |

## 手機綁定入口

以下網址是原始 `所有環境.pdf` 中的手機綁定／LIFF 入口，請依目前使用的環境選擇：

| 環境 | 手機綁定網址 | 備註 |
|---|---|---|
| Lab | [開啟 Lab 手機綁定](https://liff.line.me/2006849232-31YBmjnK) | 測試開發環境 |
| Test | [開啟 Test 手機綁定](https://liff.line.me/2006849272-a96jY93o/Bind) | 測試／驗證環境 |
| 正式區 | [開啟正式區手機綁定](https://liff.line.me/2000888624-REQZdMde/Bind) | 正式環境 |

> 原始文件未列出獨立的 Stage 手機綁定網址；如需 Stage 綁定，請先確認目前採用的 LIFF 設定，不要直接套用其他環境網址。

## 原始文件中的 QR 圖

以下圖片擷取自 `data/sources/msg/所有環境.pdf` 第 1 頁，保留原始文件中的 QR 圖，方便依現場需求掃描登入或導向：

### Test／LINE@

![MSG Test LINE@ QR Code](../assets/environment-test-line-qr.png)

### Lab／LINE@

![MSG Lab LINE@ QR Code](../assets/environment-lab-line-qr.png)

> QR 圖可能包含環境入口或 LIFF 導向資訊。使用前請確認目前所在環境，不要將 Test／Lab QR 圖誤用於正式區。

## Lab 測試商品

來源列出的銷售編號：

`1892897`、`2525814`、`2664318`、`2808740`、`3050997`、`3131478`、`3145097`、`3253698`、`3305916`

## 注意事項

- 原始文件中的資料庫帳號、密碼、Token、手機號碼與內部管理入口不複製到整理文件。
- 舊 PHP 架構的內部入口只保留「存在」的註記，不在此公開完整連線資料。
