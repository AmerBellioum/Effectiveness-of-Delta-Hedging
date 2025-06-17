#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 13:47:36 2025

@author: amerbellioum
"""

import pandas as pd

def get_market_data(asset, start_date, end_date):
    """
    Loads and cleans historical market data for each asset.

    Parameters
    ----------
    asset : list of str
        List of asset tickers (e.g., ["META", "GOOG"])
    start_date : str or pd.Timestamp
        Start of date range (e.g., "2018-01-01")
    end_date : str or pd.Timestamp
        End of date range (e.g., "2023-06-01")

    Returns
    -------
    market_data : dict
        Dictionary of cleaned DataFrames, keyed by ticker
    """
    
    market_data = {}

    for ticker in asset:
        file_path = f"/Users/amerbellioum/Documents/Derivatives_Quant_Project/{ticker}_Data.csv"
        df = pd.read_csv(file_path)

        # Convert to datetime
        df["Date"] = pd.to_datetime(df["Date"])

        # Filter by date range
        df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

        # Clean Close/Last column (remove $ or , and convert to float)
        df["Close/Last"] = (
            df["Close/Last"]
            .replace(r"[\$,]", "", regex=True)
            .astype(float)
        )

        # Optional: Reset index
        df = df.reset_index(drop=True)

        market_data[ticker] = df

    return market_data
