import pandas as pd

def get_market_data(simulation_params, contract_params):
    """
    Loads and cleans historical market data for each asset based on 
    simulation and contract parameters.
    
    Parameters
    ----------
    simulation_params : dict
        Dictionary containing simulation parameters. Relevant parameters:
            - "Start Date" (str): Start of the date range (e.g., "2017-01-01")
            - "End Date" (str): End of the date range (e.g., "2023-12-01")
    
    contract_params : dict
        Dictionary containing contract parameters. Relevant parameters:
            - "Asset" (list of str): List of asset tickers (e.g., ["META", "GOOG"])
    
    Returns
    -------
    market_data : dict
        Dictionary of cleaned pandas DataFrames, keyed by asset ticker.
        Each DataFrame contains filtered historical data between the start
        and end dates.
    """

    # 1. Extraction of Parameters from Contract / Simulation Dictionaries
    
    asset = contract_params["Asset"]
    start_date = simulation_params["Start Date"]
    end_date = simulation_params["End Date"]
    
    # 2. Construction of Output Dictionary
    
    market_data = {}

    for ticker in asset:
        
        # 2.1. Extract File & Convert to Pandas DataFrame
        
        file_path = f"/Users/amerbellioum/Documents/QuantProject_DeltaHedging/{ticker}_Data.csv"
        data = pd.read_csv(file_path)
        
        # 2.2. Convert Date Column to Datetime To Enable Arithmetic
         
        data["Date"] = pd.to_datetime(data["Date"])
        
        # 2.3. Filter Data Based on Start & End Dates
        
        data = data[(data["Date"] >= start_date) & (data["Date"] <= end_date)]
        
        # 2.4. Convert Prices from str to float
    
        data["Close/Last"] = (
            data["Close/Last"]
            .replace(r"[\$,]", "", regex=True)
            .astype(float)
        )
        data = data.reset_index(drop=True)
        market_data[ticker] = data

    return market_data

