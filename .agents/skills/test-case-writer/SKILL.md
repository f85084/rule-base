---
name: test-case-writer
description: Create simple manual QA acceptance cases for general staff and PO users from issues or requirements, with Markdown and Excel output. Use when asked to write, simplify, organize, or export test cases.
---

# Test Case Writer

把需求整理成一般人員／PO 可以照著畫面執行的功能驗收案例，並視需要輸出 Markdown 與可填寫的 `.xlsx`。本 skill 用於本專案的測試案例文件。

## Audience and boundary

- 預設讀者是一般測試人員、PO 或主管，不是 developer、SRE 或自動化測試工程師。
- 測試者只操作已提供的測試帳號與畫面；維運協助只準備合成資料、安排必要的背景動作及清理資料。
- 除非使用者明確要求技術驗收，案例步驟不要要求操作 API、JWT、Redis、SignalR、stub、HTTP status、程式碼、package、shell 或技術 log。
- 不寫入帳密、token、secret、個資、真實客戶識別資料或內部連線資訊。結果證據使用遮罩後識別碼、畫面截圖位置或測試時間。
- 未執行的 runtime 一律標示「待 QA 執行」，不可把文件閱讀、靜態檢查或自動化檢查寫成產品驗收通過。

## Workflow

1. 讀取使用者提供的需求、issue、流程文件或既有案例，先辨識需求單、功能對象、角色、可觀察畫面與限制。
2. 只把來源明確支持的行為寫進預期結果；缺少資訊時標示待確認，不自行補上固定畫面、數量、時間或重試保證。
3. 依需求拆成少量、有判定價值的案例。兩張需求單通常可採「每單約四個主要案例＋一個共同回歸」，但依實際範圍調整，不為湊數增加重複案例。
4. 優先覆蓋：正常結果、沒有新資料、通知／待辦、離線或重新登入後資料、不同使用者資料隔離、短暫中斷恢復、異常後下一筆正常資料，以及基本回歸。只保留與需求相關的情境。
5. 每案使用固定欄位：案例 ID、需求單、案例名稱、測試目的、測試角色、開始前準備、操作步驟、預期結果、通過判定、執行結果、測試日期、測試人員、證據／備註。
6. 步驟使用短句和畫面名稱；每一步只做一個動作。將背景更新、測試資料建立或特殊故障安排寫成「維運協助」的前置工作，不要求一般測試者執行技術操作。

## Output

### Markdown

以需求單或功能區分章節，每案一個標題，依固定欄位列出內容。文件開頭標明功能驗收與技術驗收的分工，以及目前 runtime 狀態。

### Excel

使用本 skill 的 `scripts/create_test_case_xlsx.py` 產生真正的 `.xlsx`，不要把 CSV 直接改副檔名。輸入 JSON 格式與欄位定義請讀 [references/case-schema.md](references/case-schema.md)。從專案根目錄執行時可使用：

```bash
python3 .agents/skills/test-case-writer/scripts/create_test_case_xlsx.py \
  --input cases.json \
  --output test-cases.xlsx
```

Excel 至少包含三個工作表：

- `測試總覽`：一案一列，方便追蹤目前狀態、執行結果、日期、人員與證據。
- `測試案例`：一案一列，放完整驗收內容及結果欄位。
- `填寫說明`：說明下拉結果、判定原則與敏感資料限制。

Excel 預設執行結果為「待 QA 執行」，並設定標題列凍結、篩選、換行、欄寬和結果下拉選項。產出後檢查：

- `zipfile.ZipFile.testzip()` 無錯誤。
- 所有 XML 可由標準 XML parser 解析，工作表名稱與案例數正確。
- `autoFilter` 位於 `dataValidations` 之前；這是 Excel 工作表 XML 的元素順序要求。
- 案例 ID 與 Markdown 或需求來源一致，沒有敏感資料。

## Handoff

回報產出的檔案、案例數、已執行的格式檢查、未執行的 runtime，以及需要 QA／PO 補充的資料。除非使用者另外授權，不 commit、push、deploy、restart 或呼叫外部服務。
