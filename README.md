## An Assessment of the Effectiveness of Daily Delta Hedging w/ Black-Scholes for Writers of European Option Contracts

Market-making financial institution that sell option contracts seek to neutralise their exposure to market movements and instead earn structural revenues (e.g., bid-ask spreads). **Delta-Hedging**, which entails holding the exact amount of shares required to offset changes in the value of the payoff, is a strategy typically employed to reduce directional exposure. However, delta-hedging itself faces multiple sources of error. Most significantly:

1. Model Error. The amount of shares held, Delta, is computed based on a mathematical model of the option price. Mathematical models are rarely fully representative - therefore there is error associated with the difference in how the MODEL values the option vs the REAL valuation. For instance, the Black-Scholes model employed in this circumstance assumes constant volatility of the underlying asset - where in reality, the volatility of the asset may be a function of time.

2. Gamma Error: 

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
