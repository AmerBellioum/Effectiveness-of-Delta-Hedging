import numpy as np
import pandas as pd


def hedgebook(delta, prices):
    """
    Hedgebook with no rebalancing on the final day.

    Parameters
    ----------
    delta : np.ndarray
        Daily delta values over the rolling window (length N)
    prices : pd.Series or np.ndarray
        Corresponding asset prices (length N)

    Returns
    -------
    hedge_cost : float
        Total cost incurred from building and adjusting the hedge
    money_held : np.ndarray
        Value of the hedge position at each time step (no rebalance on final day)
    """

    delta = np.asarray(delta)
    prices = np.asarray(prices)

    n = len(delta)
    money_held = np.zeros(n)

    # Day 0: Initial Hedge Setup
    
    hedge_cost = delta[0] * prices[0]
    money_held[0] = hedge_cost

    # Re-Balancing: t = 1 to t = n - 2
    
    d_delta = delta[1:-1] - delta[:-2]                  
    hedge_cost += np.sum(d_delta * prices[1:-1])       
    money_held[1:-1] = delta[1:-1] * prices[1:-1]

    # Final Day: No Rebalancing
    
    money_held[-1] = delta[-2] * prices[-1]

    return hedge_cost, money_held
