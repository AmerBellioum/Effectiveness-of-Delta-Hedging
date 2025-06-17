#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 12:22:54 2025

@author: amerbellioum
"""

import numpy as np
import pandas as pd


def hedgebook(delta, prices):
    """
    Vectorised hedgebook with no rebalancing on the final day.

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

    # Day 0: initial hedge setup
    hedge_cost = delta[0] * prices[0]
    money_held[0] = hedge_cost

    # Rebalancing from t = 1 to t = n - 2
    d_delta = delta[1:-1] - delta[:-2]                  # shape: (n-2,)
    hedge_cost += np.sum(d_delta * prices[1:-1])        # rebalancing costs
    money_held[1:-1] = delta[1:-1] * prices[1:-1]        # value of hedge

    # Final day: do not rebalance, use delta from t = n - 2
    money_held[-1] = delta[-2] * prices[-1]

    return hedge_cost, money_held
