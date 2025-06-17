#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 11:53:31 2025

@author: amerbellioum
"""

# Options Contract Definition & Payoff Model

import numpy as np
import matplotlib.pyplot as plt

class EuropeanOption():
    def __init__(self, S0, K, T, option_type):
        self.S0 = S0
        self.K = K
        self.T = T
        self.option_type = option_type
    
    def payoff(self, ST):
        if self.option_type == "call":
            return max(ST-self.K, 0)
        elif self.option_type == "put":
            return max(self.K - ST, 0)
        else:
            raise ValueError(f"Unsupported option type: {self.option_type}")
    
    def plot_payoff(self, ST_range=None):
        if ST_range is None:
            ST_range = np.linspace(0, 2 * self.S0, 200)
        
        payoffs = [self.payoff(ST) for ST in ST_range]
        
        plt.figure(figsize=(8,6))
        plt.plot(ST_range, payoffs)
        plt.grid()
        title = f"European {self.option_type.capitalize()} Option Payoff"
        plt.title(title)
        plt.ylabel("Payoff ($)")
        plt.xlabel("Asset Price @ Expiry ($)")
        plt.show()


if __name__ == "__main__":
    option = EuropeanOption(S0=100, K=100, T=0.5, option_type="put")
    option.plot_payoff()
