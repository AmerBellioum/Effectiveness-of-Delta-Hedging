#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 08:20:58 2025

@author: amerbellioum
"""

import numpy as np
import pandas as pd
from blackscholespricer import delta_finder

def delta_computation(data, K, r, vol, option_type="call"):
    """
    Computes delta for each time step in the data (vectorised).
    
    Parameters:
        data (DataFrame): Must include 'Close/Last' and 'Date'
        K (float): Strike
        r (float): Risk-free rate
        vol (float): Volatility
        option_type (str): 'call' or 'put'
    
    Returns:
        delta (np.ndarray): Array of deltas for each row in data
    """
    
    S = data["Close/Last"].to_numpy()                                       # Convert S to NumPy array
    tau_days = (data["Date"].iloc[-1] - data["Date"]).dt.days.to_numpy()    # Convert tau to NumPy array
    tau = tau_days / 365                                                    # Time to maturity in years

    return delta_finder(S, K, r, tau, vol, option_type)