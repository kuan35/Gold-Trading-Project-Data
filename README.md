# Gold Trading Project 私人資料交接

資料版本：2026-10-01。此 repository 必須維持 private，包含個人對帳單及逐筆交易。公開程式：[Gold-Trading-Project](https://github.com/kuan35/Gold-Trading-Project)，此資料快照對應程式 commit `0076b0138ee35b562bbe975dbd356c8599124f36`。

## 交接內容

| 路徑 | 內容 | 用途 |
|---|---|---|
| `raw/statements/` | 原始 HTML、Excel、CSV、PDF 共 221 檔 | 重跑解析與分群；原始資料唯讀 |
| `derived/audit_20261001/` | 本次 19 個分群、解析、重複候選、問題及雜湊產出 | 查原始證據、重現分類與匯入案例 |
| `derived/baseline_20260928/` | 前次來源 inventory | 重現新增來源比對 |
| `market/` | 23 份歷史 OHLC、事件資料、README 與舊版特徵表 | 回放行情來源及早期 ML 資料準備 |
| `runtime/private/` | `cases.json`、`bars.json`、`audit.json` | 本機產品可直接使用的真實案例、行情與分群 |
| `reference/` | 訪談、老師參考報告、原混合流程圖及產品 Word | 接續討論與了解題目沿革 |
| `data-manifest.json` | 每個資料檔的位元組數及 SHA-256 | 確認下載完整及來源版本 |

`market/` 中早期資料集與本次刷新分群是不同版本，不可直接把列數或 record ID 混用。早期 BUY/SELL 表的標籤以已觀察到下單為條件，不能當「會不會進場」資料。行情、案例與固定行為分類不等同已驗證策略。資料不是完整十年，也不是去重後独立交易數；帳戶時區未全確認。

## 最快啟動真實案例本機展示

先由資料 repository 擁有者把同學加入權限。取得存取權後，在同一父資料夾下載兩個 repository：

```powershell
git clone https://github.com/kuan35/Gold-Trading-Project.git
git clone https://github.com/kuan35/Gold-Trading-Project-Data.git
cd Gold-Trading-Project-Data
python verify_files.py
cd ../Gold-Trading-Project
New-Item -ItemType Directory -Path private -Force
Copy-Item -LiteralPath ../Gold-Trading-Project-Data/runtime/private/cases.json -Destination private/cases.json
Copy-Item -LiteralPath ../Gold-Trading-Project-Data/runtime/private/bars.json -Destination private/bars.json
Copy-Item -LiteralPath ../Gold-Trading-Project-Data/runtime/private/audit.json -Destination private/audit.json
```

這三份是可重建的匯入結果；複製會取代現有同名私人資料，請先備份自行改過的版本。接著依公開程式 README 安裝 Python／Node 依賴及啟動後端。GitHub Pages 本身依舊使用合成回放；私人資料只用於本機後端，不會自動發布到 Pages。

## 重新分群及匯入

以下在 `Gold-Trading-Project` 程式根目錄執行；輸出 `private/audit_rebuild_20261001` 必須是新的資料夾，不能覆寫已有稽核。

```powershell
.\.venv\Scripts\python.exe -m pip install -r research/requirements.txt
.\.venv\Scripts\python.exe research/scripts/refresh_trade_case_data.py --input ../Gold-Trading-Project-Data/raw/statements --baseline ../Gold-Trading-Project-Data/derived/baseline_20260928/source_inventory.csv --output private/audit_rebuild_20261001
.\.venv\Scripts\python.exe scripts/import_private_data.py --audit-dir private/audit_rebuild_20261001 --bars ../Gold-Trading-Project-Data/market/xauusd_5m_bars.csv --market-start 2025-10-01 --days 10
```

前端展示的歷史獲利比例只描述匹配案例池，不是新訂單預測勝率。可見首筆不代表帳戶確定空手，同分鐘順序不明與跨來源重複仍保留限制。案例時區尚未核對，不能直接聲稱 K 線形狀相似。

## Word 與進度

`reference/黃金交易輔助平台專題報告_v1.docx` 是產品型專題報告（標楷體、至少 12pt）。較晚新增的免費 TradingView 看盤與 LLM 訂閱路線，請另讀公開程式 `docs/live-chart-and-llm.md`；未把上述功能說成已完成券商／LLM 串接。

交接不含 API key、token、憑證、`.env`、電腦日誌、依賴安裝目錄或瀏覽器登入資訊。同學需要自行建立開發環境；外部 LLM 與券商 DEMO 尚未驗收。
