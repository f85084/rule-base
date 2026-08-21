# Test case input schema

`create_test_case_xlsx.py` 接受 UTF-8 JSON。最外層可包含 `title` 和必要的 `cases` 陣列：

```json
{
  "title": "CSP 功能驗收測試案例",
  "cases": [
    {
      "id": "TC-001",
      "ticket": "#12345",
      "name": "新資料顯示",
      "purpose": "確認新資料會出現在正確畫面。",
      "roles": "一般人員；PO；維運協助",
      "preparation": "維運協助準備合成測試資料。",
      "steps": ["登入系統。", "開啟指定頁面。", "重新整理並查看資料。"],
      "expected": "資料出現在正確位置，內容與準備資料相符。",
      "pass_criteria": "資料正確且沒有重複或串到其他使用者。",
      "result": "待 QA 執行",
      "test_date": "",
      "tester": "",
      "evidence": ""
    }
  ]
}
```

必要欄位：`id`、`ticket`、`name`、`purpose`、`roles`、`preparation`、`steps`、`expected`、`pass_criteria`。`steps` 可為字串或字串陣列；日期、人員、證據和結果可留白，但結果預設為「待 QA 執行」。

輸出欄位順序：

`案例 ID`、`需求單`、`案例名稱`、`測試目的`、`測試角色`、`開始前準備`、`操作步驟`、`預期結果`、`通過判定`、`執行結果`、`測試日期`、`測試人員`、`證據／備註`。
