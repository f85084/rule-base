# CSP 排錯資料說明

本層是 RuleBase 的「症狀導向排查手冊」，整理遇到特定使用者症狀時，應如何判斷現象、比對資料及排除常見誤判。文件以可快速查閱、可直接執行的排查步驟為主。

## 與 `project-docs` 的差異

完整的 CSP 業務流程、技術解析與歷史 Incident／Gotcha 仍以 `project-docs` 為主要來源，尤其是：

```text
/home/art/openab-repos/project-docs/projects/CSP/data/gotchas/incidents/
```

兩者定位如下：

| 位置 | 定位 | 內容重點 |
|---|---|---|
| `rule-base/docs/csp/troubleshooting/` | 快速排錯入口 | 依症狀提供判斷順序、必要比對項目與常見誤判提醒 |
| `project-docs/projects/CSP/data/gotchas/incidents/` | 完整 Incident／Gotcha 知識庫 | 事件時間線、Log／Trace 證據、呼叫鏈、根因、影響範圍、未知項目與後續修復 |

因此，本層不應複製 `project-docs` 的所有異常案例；需要完整事件背景時，應從這裡連回對應的 Incident 文件。

## 音檔案例的差異

- [音檔：索引與檔案建立時間落差](audio-index-delay.md)：索引先建立、NAS 音檔稍後才產生，屬於暫時性的索引／檔案同步時間差。
- [`project-docs` 2026-07-17-003：同一 ConnectionId 對應多段錄音與播放清單去重](../../../../project-docs/projects/CSP/data/gotchas/incidents/2026-07-17-003_recording-same-connectionid-multiple-segments.md)：同一通電話轉接後可能有不同 Channel 的多段錄音，問題在 `ConnectionId` 與 `RecordId` 的識別／播放清單去重，不是音檔尚未生成。

遇到音檔問題時，先判斷是「檔案尚未產生」還是「同一通話有多段錄音／去重鍵不正確」，再決定查本層排錯文件或 `project-docs` 的完整 Incident。

## 維護原則

1. 可重複套用的排查方法放在本層。
2. 來源文件中的操作細節、錯誤條件、例外情境、聯絡資料與處理方式都要保留；不可因判斷「不需要」而自行省略。若內容過長，應拆成多份文件並以索引串接。
3. 單一事件的完整調查紀錄放在 `project-docs`，但本層若引用該事件，仍須保留使用者排查所需的必要細節。
4. 若本層與 `project-docs` 都需要提到同一案例，本層保留可執行的完整排查內容與連結，避免建立兩份不同步的根因說明。
