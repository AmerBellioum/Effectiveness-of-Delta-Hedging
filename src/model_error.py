#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 16:16:16 2025

@author: amerbellioum
"""

import numpy as np
import pandas as pd
from blackscholespricer import gamma_finder    

def get_gamma_error(data, K, r, vol, option_type):
    """
    Compute gamma error over a rolling window of market data.
    
    Parameters
    ----------
    data : pd.DataFrame
        Must contain 'Close/Last' and 'Date' columns (ascending order).
    K : float
        Strike price.
    r : float
        Risk-free rate.
    vol : float
        Volatility.
    option_type : str
        'call' or 'put'.
    
    Returns
    -------
    gamma_error : float
        Total gamma error over the window.
    """

    S = data["Close/Last"].to_numpy()
    tau_days = (data["Date"].iloc[-1] - data["Date"]).dt.days.to_numpy()
    tau = tau_days / 365

    gamma = gamma_finder(S, K, r, tau, vol, option_type)

    delta_S = np.diff(S)

    # Gamma[1:] aligns with ΔS[1:] for k = 1 to n-1
    gamma_core = gamma[1:-1]
    delta_S_core = delta_S[1:]

    # Gamma Error calculation
    gamma_error = 0.5 * np.sum(gamma_core * delta_S_core**2)

    return gamma_error
