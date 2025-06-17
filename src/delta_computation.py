import numpy as np
import pandas as pd
from blackscholespricer import delta_finder

def delta_computation(data, K, r, vol, option_type):
    """
    Computes delta for each time step in the data (vectorised).
    
    Parameters:
        data (DataFrame): Window of Market Data
        K (float): Strike
        r (float): Risk-free rate
        vol (float): Volatility
        option_type (str): 'call' or 'put'
    
    Returns:
        delta (np.ndarray): Array of deltas for each row in data
    """
    
    S = data["Close/Last"].to_numpy()                                       
    tau_days = (data["Date"].iloc[-1] - data["Date"]).dt.days.to_numpy()
    tau = tau_days / 365
    
    return delta_finder(S, K, r, tau, vol, option_type)
