# 決策點資料集說明

每一列是一筆真實的 XAU/USD 進場決策，對到當天（依券商時間正確換算成 UTC 交易日，
不是拿日期字串直接比對）的 Layer 1 市場特徵。

## 兩個檔案

- `decision_point_dataset_v1_no_indicators.csv`：不含技術指標
- `decision_point_dataset_v2_with_indicators.csv`：v1 全部欄位 + RSI/MACD/布林通道/ATR

兩份檔案的 `record_id`、列數、順序完全一樣，只差 8 個技術指標欄位，
跟 `layer1_features_v1/v2` 的邏輯一致。

- 成功對上：3310 筆
- 因為券商時區未驗證而排除（Lirunex）：74 筆
- 對不到市場資料或缺開倉時間：0 筆，詳見 `decision_point_join_issues.csv`

## 欄位

- `label_*`：交易員實際的動作（方向、手數、停損停利、損益）——**這是訓練目標，
  絕對不能拿來當模型輸入特徵**，不然就是把答案洩漏進特徵裡
- `feature_*`（市場面）：對應交易日的市場特徵（均線、技術指標等），全部只用該日
  及之前的資料算出，符合 point-in-time
- `feature_trading_window`：這筆交易落在交易員自己說的哪個台灣時間交易時段
  （"09:30"／"18:00"／"00:00"／空字串＝都不在），直接用交易本身的時間換算，
  不需要額外市場資料
- `feature_minutes_to_major_event`：距離下一個美元高影響力經濟數據還有幾分鐘。
  2021-01-06～2025-04-07 這段用 Hugging Face 上 `Ehsanrs2/Forex_Factory_Calendar`
  資料集（MIT授權，ForexFactory歷史存檔，已篩選Currency=USD、Impact=High），
  涵蓋FOMC決議、CPI、NFP、零售銷售、GDP、Fed官員談話等；**2025-04-07之後**這個
  資料集沒有涵蓋，改用FOMC＋NFP的固定清單頂著，見下方限制
- `feature_cumulative_same_direction_lot`／`feature_add_count_same_direction`：
  下這筆單的當下，同帳戶、同方向還「開著」的單，加總手數／這是第幾次加碼
  （只看這筆單自己之前的紀錄，不看後面發生的事）
- `feature_unrealized_pnl_estimate_usd`：下這筆單的當下，同帳戶同方向所有未平倉
  部位的估計浮動損益——**用「前一個交易日」的收盤價估計，不是真正下單當下的
  即時報價**（因為市場資料只有日線），只是近似值
- `trading_day_utc`：換算後的正確 UTC 交易日，用這個去對市場資料，不要用
  `open_time_broker_raw`／`open_time_broker` 的日期部分直接比對

## 限制

- 只涵蓋已確認伺服器時區的四家券商，Lirunex 還沒驗證，排除在外
- DST 切換日用歐盟標準規則假設，尚未拿券商設定畫面精確鎖定
- 市場特徵目前只有日線，短週期（1H/15-30分/1-5分）特徵還沒接進來
- `feature_minutes_to_major_event`：2025-04-07 之後只剩 FOMC＋NFP 兩種事件，
  比前面那段（有完整高影響力事件清單）稀疏，這段時間該欄位會偏保守（低估風險）
- 經濟數據行事曆的原始資料是別人爬蟲整理好公開放上 Hugging Face 的（非官方），
  不是我們自己爬的，也不是官方來源，數值可能有極少數缺漏或誤植
- `feature_unrealized_pnl_estimate_usd` 用前一日收盤價估計，不是真實即時損益，
  且假設每口 100 盎司（XAU/USD 標準合約規格）
