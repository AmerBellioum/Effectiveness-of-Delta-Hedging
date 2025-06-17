## 📁 Data Format Requirements

For the code to work, the market data must be stored specifically as highlighted:

1. A separate '.csv' file for each asset - saved as "{TICKER}_Data.csv" (e.g., `META_Data.csv`, `GOOG_Data.csv`)
2. Each .csv file must contain data sampled at **daily frequency** only. The implementation does not support intraday, weekly, or monthly data.
3. Files must be stored in a local path.
4. The columns of the data must follow the same format as NASDAQ market data

