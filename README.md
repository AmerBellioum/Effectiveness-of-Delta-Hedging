# Effectiveness-of-Delta-Hedging
An assessment of the effectiveness of delta-hedging on the PnL made on short-selling equity options

Consider an option writer that adopts an unhedged position on a European call option. The PnL of the writer is the premium charged subtracted by the payoff.

PnL = Option Premium - max (Asset Price - Strike, 0)

If the option is exercised, the option writer can face potentially unbounded losses. If not, the option writer pockets the premium. It is clear that the option writer effectively wagers that the asset price will drop. 

However, many financial institutions selling option contracts are not looking to "bet" on the underlying asset going one way or the other. Instead, they seek to generate profits from market-making activities, such as capturing bid-ask spreads. As such, they hedge their position by holding sufficient shares of the underlying asset to offset exposure. 
