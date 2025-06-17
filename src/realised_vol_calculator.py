#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 15:11:14 2025

@author: amerbellioum
"""

import numpy as np
import pandas as pd

def realised_volatility_calculation(data):
    """
    Input:
        Data (DataFrame), Historical Data of Market Prices
        
    Output:
        Realised Volatility (Float), Volatility of Asset 
    """
    
    S = data["Close/Last"].astype(float).values   # Prices as Numpy Array
    ri = np.diff(np.log(S))                 # Log-Returns
    r_bar = np.mean(ri)             # Mean of Log-Returns
    squared_diffs = (ri - r_bar) ** 2
    sample_var = np.sum(squared_diffs) / (len(ri) - 1)
    sample_std = np.sqrt(sample_var)
    return sample_std * np.sqrt(252)  
