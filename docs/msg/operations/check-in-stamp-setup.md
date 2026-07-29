# 印章設定

## 查詢印章

```sql
SELECT * FROM stamps;
```

## 新增印章

`Id` 會由資料庫自動產生，新增時不用指定：

```sql
INSERT INTO stamps
    (name, coordinate, created_at, created_by)
VALUES
    (
        '印章名稱',
        '[{"X":120,"Y":256},{"X":242,"Y":256},{"X":242,"Y":377},{"X":120,"Y":377}]',
        NOW(),
        建立者UserId
    );
```

## 綁定活動

到 MSG B2E `/CheckIn`：

1. 找到簽到活動。
2. 點選「簽到印章設定」。
3. 選取新增的印章。
4. 按「儲存」。

## 確認測試結果

```sql
SELECT *
FROM check_in_log
ORDER BY created_at DESC
LIMIT 10;
```

如果沒有紀錄，先確認印章是否已在活動的「簽到印章設定」中儲存，並重新開啟 B2C 簽到頁。

完整的點位取得方式、資料表關聯、API 流程與容許值說明，請查看 `project-docs/projects/MSG/data/business-flows/B2E/L1/CheckIn.md`。
