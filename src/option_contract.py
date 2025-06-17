import numpy as np
import matplotlib.pyplot as plt

class european_option:
    """
    Class representing European-style option contract.

    Attributes
    ----------
    S0 : float
        Initial asset price.
    K : float
        Strike price of the option.
    T : float
        Time to maturity (in years).
    option_type : str
        Type of option ('call' or 'put').
    """

    def __init__(self, S0, K, T, option_type):
        """
        Initialises the european_option object.

        Parameters
        ----------
        S0 : float
            Initial asset price.
        K : float
            Strike price.
        T : int
            Time to maturity (in years).
        option_type : str
            Type of option ('call' or 'put').
        """
        
        self.S0 = S0
        self.K = K
        self.T = T
        self.option_type = option_type
    
    def payoff(self, ST):
        """
        Computes the payoff of the option at expiry.

        Parameters
        ----------
        ST : float
            Asset price at expiry.

        Returns
        -------
        float
            Payoff value of the option.
        """
        
        if self.option_type == "call":
            return max(ST - self.K, 0)
        elif self.option_type == "put":
            return max(self.K - ST, 0)
        else:
            raise ValueError(f"Unsupported option type: {self.option_type}")
    
    def plot_payoff(self, ST_range=None):
        """
        Plots the payoff profile of the option over a range of asset prices.

        Parameters
        ----------
        ST_range : array-like, optional
            Range of asset prices at expiry to evaluate payoff.
            If None, defaults to np.linspace(0, 2 * S0, 200).
        """
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
