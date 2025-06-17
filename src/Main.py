#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 12:59:52 2025

@author: amerbellioum
"""

# PROJECT: The Effectiveness of Discrete Delta-Hedging for European Call Option Writer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Python Libraries Imported

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import Axes3D
from Get_Market_Data import get_market_data
from blackscholespricer import BS_optionprice
from blackscholespricer import delta_finder
from get_rolling_windows import get_rolling_windows
from delta_computation import delta_computation
from hedge_book import hedgebook
from OptionContract import EuropeanOption
from surface_plotting import surface_plotting
from realised_vol_calculator import realised_volatility_calculation
from model_error import get_gamma_error

# Inputs 
# ~~~~~

# Fixed Variables:
# Start-To-End Date of Data
# Rolling Window

start_date = "2017-01-01"                           # Start Date for Historical Data
end_date = "2023-12-31"                             # End Date for Historical Data
rw = 20                                             # Rolling Window (Day)
ra = 1.645                                          # Risk Aversion
vol = 0.2                                           # Estimated Volatility (Constant)
r = 0.05                                            # Risk-Free Interest Rate 

# Control Variables:
# Underlying Asset, Time to Maturity, Moneyness of Contract, Option Type

asset = ["META", "GOOG", "AMZN"]                    # Underlying Asset Tickers 
T = np.linspace(1, 48, 50)/24                       # Time to Maturity (Years)
T_abs = T * 365                                     # Time to Maturity (Days)
T_trading = (T * 252).astype(int)                   # Time to Maturity (Trading Days)
option_type = "call"                                # Option Type
S0_K = np.linspace(0.7, 1.3, 50)                    # Moneyness Levels (Spot Price / Strike Price)

# Outputs:
# ~~~~~

# Dictionary of Market Data
# Pre-Requisite: Market Data To Be Stored as {TICKER}_Data.csv

market_data = get_market_data(asset, start_date, end_date)

# Main Data Processing
# ~~~~~

PnL_records = []                                        # Profits & Losses

for ticker in asset:
    ticker_data = market_data[f"{ticker}"]                          # Loads Ticker Market Data (DataFrame)
    for maturity in T_trading:
        windows = get_rolling_windows(ticker_data, maturity, rw)    # Forward-Looking Rolling Window Dictionary Created
        for money in S0_K:
            for roll in windows:
                
                # Output 1 - Hedge Effectiveness
                
                data = windows[roll]                                                                                    # DataFrame of One Rolling Window
                S = data["Close/Last"]
                K = data["Close/Last"].iloc[0] / money                                                                  # Strike Price ($)
                contract = EuropeanOption(S.iloc[0], K, maturity, option_type)
                payoff = contract.payoff(S.iloc[-1])
                option_price = BS_optionprice(S.iloc[0], K, r, maturity/252, vol, option_type)                          # Option Price ($)
                delta = delta_computation(data, K, r, vol, option_type)                                       # Daily Delta 
                hedge_cost, money_held = hedgebook(delta, S)                                                            # Hedge Cost
                PnL = option_price - hedge_cost - payoff + money_held[-1] # PnL for a given rolling window              # PnL
                
                # Output 2 - Diagnostics
                
                # Diagnostic 1 - Volatility Mis-Pricing
                
                real_vol = realised_volatility_calculation(data)
                option_price_real = BS_optionprice(S.iloc[0], K, r, maturity, real_vol, option_type)
                vol_mispricing = option_price_real - option_price
                
                # Diagnostic 2 - Gamma Error
                
                gamma_error = get_gamma_error(data, K, r, vol, option_type)
                
                # Diagnostic 3 - Residual Error

                                
                # Append
                
                PnL_records.append({
                    "Ticker": ticker,
                    "Maturity (days)": maturity,
                    "Moneyness": money,
                    "Start Date": roll,
                    "Option Price": option_price,
                    "PnL": PnL,
                    "Realised Volatility": real_vol,
                    "Volatility Mispricing": vol_mispricing,
                    "Gamma Error": gamma_error
                    })
                
                
# Data Post-Processing
# ~~~~~

PnL_dataframe = pd.DataFrame(PnL_records) # List of Dictionaries to DataFrame

# Group across all contracts and assets — only by date
vol_time_global = PnL_dataframe.groupby("Start Date")["Realised Volatility"].mean().reset_index()

# Plot
plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(20, 12))
ax.plot(vol_time_global["Start Date"], vol_time_global["Realised Volatility"],
        label="Average Realised Volatility", linewidth=2.5, color="darkgreen")

# Add mean line
ax.axhline(y=vol_time_global["Realised Volatility"].mean(), color='black',
           linestyle='--', linewidth=1.5, label="Overall Mean Volatility")

# Title and labels
ax.set_title("Average Realised Volatility Over Time\n(Computed from Rolling Windows Across All Contracts & Assets)",
             fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel("Rolling Window Start Date", fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel("Realised Volatility (%)", fontsize=14, fontweight='bold', labelpad=10)

# Axis ticks and formatting
ax.legend(fontsize=12)
ax.tick_params(axis='both', labelsize=12)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# 1st Plot - Long Maturity, ATM Contract Plotted vs. Time for different Assets

PnL_time_META = PnL_dataframe[(PnL_dataframe["Maturity (days)"] == T_trading[-1]) & (PnL_dataframe["Moneyness"] == S0_K[len(S0_K) // 2]) & (PnL_dataframe["Ticker"] == "META")]
PnL_time_GOOG = PnL_dataframe[(PnL_dataframe["Maturity (days)"] == T_trading[-1]) & (PnL_dataframe["Moneyness"] == S0_K[len(S0_K) // 2]) & (PnL_dataframe["Ticker"] == "GOOG")]
PnL_time_AMZN = PnL_dataframe[(PnL_dataframe["Maturity (days)"] == T_trading[-1]) & (PnL_dataframe["Moneyness"] == S0_K[len(S0_K) // 2]) & (PnL_dataframe["Ticker"] == "AMZN")]

plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(20, 12))
ax.plot(PnL_time_META["Start Date"], PnL_time_META["PnL"], label="META", linewidth=2.5)
ax.plot(PnL_time_GOOG["Start Date"], PnL_time_GOOG["PnL"], label="GOOG", linewidth=2.5)
ax.plot(PnL_time_AMZN["Start Date"], PnL_time_AMZN["PnL"], label="AMZN", linewidth=2.5)

ax.axhline(0, color='black', linewidth=1, linestyle='--')

ax.set_title("PnL Over Time – 2Y ATM Option Across Different Assets", fontsize=14, fontweight='bold')
ax.set_xlabel("Date", fontsize=12, fontweight='bold')
ax.set_ylabel("PnL", fontsize=12, fontweight='bold')

ax.legend(fontsize=11)
ax.tick_params(axis='both', labelsize=11)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# 2nd Plot - META Contract Plotted vs Time. vs. Contracts

# 2.1. Different Time to Maturity

PnL_time_META_C1 = PnL_dataframe[(PnL_dataframe["Maturity (days)"] == T_trading[1]) & (PnL_dataframe["Moneyness"] == S0_K[len(S0_K) // 2]) & (PnL_dataframe["Ticker"] == "META")]
PnL_time_META_C2 = PnL_dataframe[(PnL_dataframe["Maturity (days)"] == T_trading[-1]) & (PnL_dataframe["Moneyness"] == S0_K[len(S0_K) // 2]) & (PnL_dataframe["Ticker"] == "META")]
PnL_time_META_C3 = PnL_dataframe[(PnL_dataframe["Maturity (days)"] == T_trading[len(T_trading) // 2]) & (PnL_dataframe["Moneyness"] == S0_K[len(S0_K) // 2]) & (PnL_dataframe["Ticker"] == "META")]

# 2.2. Different Moneyness

PnL_time_META_C4 = PnL_dataframe[(PnL_dataframe["Maturity (days)"] == T_trading[-1]) & (PnL_dataframe["Moneyness"] == S0_K[1]) & (PnL_dataframe["Ticker"] == "META")]
PnL_time_META_C5 = PnL_dataframe[(PnL_dataframe["Maturity (days)"] == T_trading[-1]) & (PnL_dataframe["Moneyness"] == S0_K[-1]) & (PnL_dataframe["Ticker"] == "META")]
PnL_time_META_C6 = PnL_dataframe[(PnL_dataframe["Maturity (days)"] == T_trading[-1]) & (PnL_dataframe["Moneyness"] == S0_K[len(S0_K) // 2]) & (PnL_dataframe["Ticker"] == "META")]

plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(20, 12))

ax.plot(PnL_time_META_C1["Start Date"], PnL_time_META_C1["PnL"], label="T = 0.5M, ATM", linewidth=2.5)
ax.plot(PnL_time_META_C2["Start Date"], PnL_time_META_C2["PnL"], label="T = 2Y, ATM", linewidth=2.5)
ax.plot(PnL_time_META_C3["Start Date"], PnL_time_META_C3["PnL"], label="T = 1Y, ATM", linewidth=2.5)
ax.plot(PnL_time_META_C4["Start Date"], PnL_time_META_C4["PnL"], label="T = 2Y, OTM", linewidth=2.5)
ax.plot(PnL_time_META_C5["Start Date"], PnL_time_META_C5["PnL"], label="T = 2Y, Deep ITM", linewidth=2.5)

ax.axhline(0, color='black', linewidth=1, linestyle='--')

ax.set_title("PnL Over Time – META Options with Varying Characteristics", fontsize=14, fontweight='bold')
ax.set_xlabel("Date", fontsize=12, fontweight='bold')
ax.set_ylabel("PnL", fontsize=12, fontweight='bold')

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)

ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax.legend(fontsize=11)
ax.tick_params(axis='both', labelsize=11)

plt.tight_layout()
plt.show()

# 3rd Plot - Mean PnL, Option Price, Std PnL, Volatility Premium

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

# 4th Plot - Volatility Mispricing (Mean)
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

# 5th Plot - Gamma Error (Mean)
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


