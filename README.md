## 📁 Market Data Format Requirements

For the code to work, the market data must be stored specifically as highlighted:

1. A separate '.csv' file for each asset - saved as "{TICKER}_Data.csv" (e.g., `META_Data.csv`, `GOOG_Data.csv`)
2. Each .csv file must contain data sampled at **daily frequency** only. The implementation does not support intraday, weekly, or monthly data.
3. The data must contain only trading days. 
4. The data must have exactly the same format as shown in the sample below. 
5. Files must be stored in a local path.

**Sample Market Data Format**:

<p align="center">
  <img src="figures/Market_Data_Format.png" width="500"/>
</p>
