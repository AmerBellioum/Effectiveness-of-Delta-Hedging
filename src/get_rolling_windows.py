#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 14:43:45 2025

@author: amerbellioum
"""

import pandas as pd

def get_rolling_windows(ticker_data, T, rw):
    """
    Input:
        Ticker Data (DataFrame):
            DataFrame of Market Data for Ticker
        T, Time to Maturity (integer):
            Time to Maturity in Trading Days
        rw, Rolling Window (integer):
            Rolling Window in Days
    Output:
        Rolling Windows (Dictionary of Dataframes):
            Dictionary of Dataframes corresponding to time periods
    """
    
    windows = {}                                                                            # Dictionary Initialised
    ticker_data["Date"] = pd.to_datetime(ticker_data["Date"])                               # Trading Dates Numerised
    ticker_data = ticker_data.sort_values("Date", ascending=True).reset_index(drop=True)    # Dates Flipped (Start Date to Expiry)


    # While Loop 
    # -> Creates rolling windows until not enough dates left.
    
    k = 0 
    while k + T <= len(ticker_data):
        rolling_series = ticker_data.iloc[k :(k + T)]           # Rolling Series of Data
        start_date = rolling_series.iloc[0]["Date"]            # Start Date of Window
        windows[start_date] = rolling_series                    # Appended to Dict.
        
        k += rw
        
    return windows


