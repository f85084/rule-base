# 測試資料：訂單質檢

來源：`訂單質檢.pdf`

## 測試帳號

| 帳號 | 員編 | 角色 |
|---|---:|---|
| qatest1 | 382545 | 系統分派之組長 1 |
| qatest2 | 382546 | 系統分派之組長 2 |
| qatest3 | 382547 | 專員組長 |
| qatest4 | 382548 | 專員處長 |
| obtest | 382388 | 質檢小組成員 |
| obtest2 | 382391 | 質檢小組主管 |

## 測試案例

| 測試項目 | 流程 | 驗證結果 |
|---|---|---|
| 缺失判斷（手動） | 懲處 → 確認 → 上訴 → 結案 | 依選擇紀錄缺失；`order_qa.mistake` 應為缺失組長員編 |
| 缺失判斷（手動） | 懲處 → 確認 → 上訴 → 複核 → 結案 | 依選擇紀錄缺失；`order_qa.mistake` 應為缺失組長員編 |
| 缺失判斷（自動） | 正常（組長 1） → 懲處（組長 2） → 確認 → 懲處 | `order_qa.mistake` 應記錄組長 1 的員編 |
| 案件正常結案 | 正常（組長 1） → 正常（組長 2） | 案件結案；`order_qa.resultType` 應為 `2`（關聯 `OrderEnum.QAResultType`） |

## 質檢單初始化

前提：`order_qa.AgentId` 為 `382519`；Lab 已設定該專員的部門組級主管為 `qatest3`、處級主管為 `qatest4`。

| 欄位 | 初始值 | 說明 |
|---|---|---|
| `order_qa.AgentId` | `382519` | 質檢單所屬專員 |
| `order_qa.leader1` | `382545` | 系統分派的第一位組長（`qatest1`） |
| `order_qa.leader2` | `382546` | 系統分派的第二位組長（`qatest2`） |
| `order_qa.leader` | `382545` | 質檢者；預設為第一位系統分派組長 |
| `order_qa.assignTo` | `382545` | 目前處理人員；預設為第一位系統分派組長 |
| `order_qa.resultType` | `0` | 未結案 |
| `order_qa.times` | `1` | 當前質檢單執行流程的次數 |
| `order_qa.nextFlowKey` | `init-1` | 對應設定檔中的第一個 key |
