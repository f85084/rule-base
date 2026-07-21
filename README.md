# RuleBase

RuleBase 是 CSP / MSG 等專案的**統一業務規則與測試資料知識庫**。

## 目標

將散落在各處的商業邏輯、測試資料與專案文件，轉換為可被 AI 檢索、可執行判斷、可統一管理的結構化知識。

## 三種核心用途

1. **RAG 知識庫** — 讓 AI 能語意檢索專案規則、測試案例與業務流程。
2. **測試資料管理** — 統一管理各領域的測試資料，並與規則綁定。
3. **規則引擎** — 將商業邏輯結構化為可執行的規則描述。

## 與現有文件的關係

RuleBase **不取代** `project-docs/projects/CSP/data/business-flows` 等現有文件，而是把它們作為輸入來源：

- `business-flows`（L1/L2/L3/special）→ 文件片段、技術鏈路、業務流程
- 原始碼 → 程式實作細節
- 測試案例 → 結構化測試資料
- 專家知識 → 可執行規則

## 目錄結構

```
RuleBase/
├── docs/               # 設計與架構文件、測試資料參考表
├── data/               # 靜態資料與規則定義
│   ├── rules/          # 規則與領域知識結構
│   ├── samples/        # 測試資料樣本
│   └── sources/        # 原始參考文件（PDF、OneNote 匯出檔等）
├── engine/             # 規則執行程式碼
├── tools/              # 資料匯入、同步、驗證、RAG 索引等工具
└── scripts/            # 一次性或輔助腳本
```

## 已整理文件

- 測試資料索引：`docs/test-data.md`
- 商業規則：`docs/business-rules-pickup.md`
- 軟體電話：`docs/softphone.md`
- 音檔調聽與排查：`docs/audio-recordings.md`、`docs/audio-index-delay.md`

## 狀態

目前為最小可行雛形（MVP skeleton），僅建立基本目錄與架構文件。
