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
    
    windows = {}                                                                            
    ticker_data = ticker_data.sort_values("Date", ascending=True).reset_index(drop=True)

    # While Loop: Rolling Windows Developed
    
    k = 0 
    while k + T <= len(ticker_data):
        rolling_series = ticker_data.iloc[k :(k + T)]           
        start_date = rolling_series.iloc[0]["Date"]             
        windows[start_date] = rolling_series                  
        
        k += rw
        
    return windows


