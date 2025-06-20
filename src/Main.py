# PROJECT: The Effectiveness of Discrete Delta-Hedging for European Call Option Writer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Python Libraries
# ~~~~~

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Get_Market_Data import get_market_data
from get_rolling_windows import get_rolling_windows
from option_contract import european_option
from blackscholespricer import BS_optionprice
from blackscholespricer import delta_finder
from delta_computation import delta_computation
from hedge_book import hedgebook
from realised_vol_calculator import realised_volatility_calculation
from model_error import get_gamma_error
from mpl_toolkits.mplot3d import Axes3D
from surface_plotting import surface_plotting

# Inputs 
# ~~~~~

simulation_params = {
    "Start Date": "2017-01-01",
    "End Date": "2023-12-31",
    "Rolling Window": 20,
    "Risk Aversion Coeff.": 1.645,
    "Estimated Volatility": 0.2,
    "Risk-Free Interest Rate": 0.05
    }

contract_params = {
    "Asset": ["META", "GOOG", "AMZN"],
    "Option Type": "call",
    "Time To Maturity (Years) Range": np.linspace(1/24,48/24,50),
    "Moneyness Range": np.linspace(0.7, 1.3, 50)
    }
 
# ~~~~~

# Data Handling
# ~~~~~

# 1. Generation of Relevant Market Data (Dictionary)

market_data = get_market_data(simulation_params, contract_params)

# 2. Core Simulation Engine

PnL_records = []                                        

for ticker in contract_params["Asset"]:
    ticker_data = market_data[f"{ticker}"]
    print(ticker)
    for maturity in contract_params["Time To Maturity (Years) Range"]:
        print(maturity)
        windows = get_rolling_windows(ticker_data, maturity, simulation_params["Rolling Window"])    
        for money in contract_params["Moneyness Range"]:
            for roll in windows:
                data = windows[roll]
                
                maturity_d = maturity * 365
                
                # Trading Days -> Years
                
                # Historical Asset Prices & Contract Strike Price

                S = data["Close/Last"]
                K = data["Close/Last"].iloc[0] / money
                
                # Option Contract & Payoff
                
                contract = european_option(S.iloc[0], K, maturity, contract_params["Option Type"])
                payoff = contract.payoff(S.iloc[-1])
                
                # Option Valuation w/ Black-Scholes
                
                option_price = BS_optionprice(S.iloc[0], K, simulation_params["Risk-Free Interest Rate"], maturity, simulation_params["Estimated Volatility"], contract_params["Option Type"])
                delta = delta_computation(data, K, simulation_params["Risk-Free Interest Rate"], simulation_params["Estimated Volatility"], contract_params["Option Type"])     
     
                # Hedging Costs

                hedge_cost, money_held = hedgebook(delta, S)
                
                # Output 1: Hedge Effectiveness - PnL of Hedging Strategy
            
                PnL = option_price - hedge_cost - payoff + money_held[-1]
                
                # Output 2 - Diagnostics
                
                # Diagnostic 1 - Volatility Mis-Pricing
                
                real_vol = realised_volatility_calculation(data)
                option_price_real = BS_optionprice(S.iloc[0], K, simulation_params["Risk-Free Interest Rate"], maturity, real_vol, contract_params["Option Type"])
                vol_mispricing = option_price_real - option_price
                
                # Diagnostic 2 - Gamma Error
                
                gamma_error = get_gamma_error(data, K, simulation_params["Risk-Free Interest Rate"], simulation_params["Estimated Volatility"], contract_params["Option Type"])
            
                # Append
                
                PnL_records.append({
                    "Ticker": ticker,
                    "Maturity (days)": maturity_d,
                    "Moneyness": money,
                    "Start Date": roll,
                    "Option Price": option_price,
                    "PnL": PnL,
                    "Realised Volatility": real_vol,
                    "Volatility Mispricing": vol_mispricing,
                    "Gamma Error": gamma_error
                    })
# ~~~~~

# Data Post-Processing
# ~~~~~

PnL_dataframe = pd.DataFrame(PnL_records)  # List of Dictionaries to DataFrame

# Extraction of Plotting Parameters

T_days = contract_params["Time To Maturity (Years) Range"] * 365
moneyness_range = contract_params["Moneyness Range"]
ra = simulation_params["Risk Aversion Coeff."]

# 1st Plot - Long Maturity, ATM Contract Plotted vs. Time for different Assets

longest_maturity = T_days[-1]
atm_moneyness = moneyness_range[len(moneyness_range) // 2]

PnL_time_META = PnL_dataframe[
    (PnL_dataframe["Maturity (days)"] == longest_maturity) & 
    (PnL_dataframe["Moneyness"] == atm_moneyness) & 
    (PnL_dataframe["Ticker"] == "META")
]
PnL_time_GOOG = PnL_dataframe[
    (PnL_dataframe["Maturity (days)"] == longest_maturity) & 
    (PnL_dataframe["Moneyness"] == atm_moneyness) & 
    (PnL_dataframe["Ticker"] == "GOOG")
]
PnL_time_AMZN = PnL_dataframe[
    (PnL_dataframe["Maturity (days)"] == longest_maturity) & 
    (PnL_dataframe["Moneyness"] == atm_moneyness) & 
    (PnL_dataframe["Ticker"] == "AMZN")
]

plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(20, 12))
ax.plot(PnL_time_META["Start Date"], PnL_time_META["PnL"], label="META", linewidth=2.5)
ax.plot(PnL_time_GOOG["Start Date"], PnL_time_GOOG["PnL"], label="GOOG", linewidth=2.5)
ax.plot(PnL_time_AMZN["Start Date"], PnL_time_AMZN["PnL"], label="AMZN", linewidth=2.5)

ax.axhline(0, color='black', linewidth=1, linestyle='--')

ax.set_title(f"PnL Over Time – {longest_maturity}D ATM Option Across Different Assets", fontsize=14, fontweight='bold')
ax.set_xlabel("Date", fontsize=12, fontweight='bold')
ax.set_ylabel("PnL", fontsize=12, fontweight='bold')

ax.legend(fontsize=11)
ax.tick_params(axis='both', labelsize=11)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# 2. Set of Plots - Mean PnL, Option Price, Std PnL, Volatility Premium

mean_PnL = PnL_dataframe.groupby(["Maturity (days)", "Moneyness"])["PnL"].mean().reset_index(name="Mean PnL")
optionprice = PnL_dataframe.groupby(["Maturity (days)", "Moneyness"])["Option Price"].mean().reset_index(name="Option Price")
std_PnL = PnL_dataframe.groupby(["Maturity (days)", "Moneyness"])["PnL"].std().reset_index(name="Std. Deviation of PnL")

vol_prem = -mean_PnL["Mean PnL"] + ra * std_PnL["Std. Deviation of PnL"]
vol_prem_df = mean_PnL[["Maturity (days)", "Moneyness"]].copy()
vol_prem_df["Volatility Premium"] = vol_prem

# Plot 1 - Mean PnL
surface_plotting(
    mean_PnL,
    x_col="Moneyness",
    y_col="Maturity (days)",
    z_col="Mean PnL",
    title="3D Surface: Mean PnL",
    z_label="Mean PnL",
    cmap='viridis'
)

# Plot 2 - Std. Deviation of PnL
surface_plotting(
    std_PnL,
    x_col="Moneyness",
    y_col="Maturity (days)",
    z_col="Std. Deviation of PnL",
    title="3D Surface: Std. Deviation of PnL",
    z_label="Std. Dev of PnL",
    cmap='plasma'
)

# Plot 3 - Volatility Premium
surface_plotting(
    vol_prem_df,
    x_col="Moneyness",
    y_col="Maturity (days)",
    z_col="Volatility Premium",
    title="3D Surface: Volatility Premium",
    z_label="Volatility Premium",
    cmap='inferno'
)

# Plot - Volatility Mispricing (Mean)
mean_vol_misprice = PnL_dataframe.groupby(["Maturity (days)", "Moneyness"])["Volatility Mispricing"].mean().reset_index(name="Mean Volatility Mis-Pricing")
std_vol_misprice = PnL_dataframe.groupby(["Maturity (days)", "Moneyness"])["Volatility Mispricing"].std().reset_index(name="Std. Dev of Volatility Mis-Pricing")

surface_plotting(
    mean_vol_misprice,
    x_col="Moneyness",
    y_col="Maturity (days)",
    z_col="Mean Volatility Mis-Pricing",
    title="3D Surface: Mean Volatility Mispricing",
    z_label="Mean Volatility Mispricing",
    cmap='cividis'
)

# Plot - Gamma Error (Mean)
mean_gamma_error = PnL_dataframe.groupby(["Maturity (days)", "Moneyness"])["Gamma Error"].mean().reset_index(name="Mean Gamma Error")
std_gamma_error = PnL_dataframe.groupby(["Maturity (days)", "Moneyness"])["Gamma Error"].std().reset_index(name="Std. Dev of Gamma Error")

surface_plotting(
    mean_gamma_error,
    x_col="Moneyness",
    y_col="Maturity (days)",
    z_col="Mean Gamma Error",
    title="3D Surface: Mean Gamma Error",
    z_label="Mean Gamma Error",
    cmap='magma'
)
