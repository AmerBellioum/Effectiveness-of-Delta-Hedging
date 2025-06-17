import numpy as np
import pandas as pd

def realised_volatility_calculation(data):
    """
    Input:
        Data (DataFrame), Historical Data of Market Prices
        
    Output:
        Realised Volatility (Float), Volatility of Asset 
    """
    
    S = data["Close/Last"].astype(float).values  
    
    # Log-Returns & Mean of Log Returns
    ri = np.diff(np.log(S))                 
    r_bar = np.mean(ri)           
    
    # Realised Volatility Computation
    
    squared_diffs = (ri - r_bar) ** 2
    sample_var = np.sum(squared_diffs) / (len(ri) - 1)
    sample_std = np.sqrt(sample_var)
    return sample_std * np.sqrt(252)  
