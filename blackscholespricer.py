#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 08:28:11 2025

@author: amerbellioum
"""

# Black Scholes Pricing

import numpy as  np
from scipy.stats import norm

def BS_optionprice(S0, K, r, T, vol, option_type):
    """
    Parameters:
    ----------
    S0 (float): Initial Asset Price in $ (Must be Positive)
    K (float): Strike Price in $ (Must be Positive)
    r (float): Risk-Free Interest Rate in % per annum 
    T (float): Time to Expiration in Years (Must be Positive)
    vol (float): Volatility per annum (Must be Positive)
    Option Type (string): What type of option it is. ("call" or "put")
    
    Raises:
    - Value Error: If inputs are invalid
    
    Returns:
    - c (float): Price of call option in $  - If Call Option
    - p (float): Price of put option in $ - If Put Option

    """
    if S0 < 0:
        raise ValueError("Initial asset price must be positive.")
    if K <= 0:
        raise ValueError("Strike price must be positive.")
    if T <= 0:
        raise ValueError("Time to expiration must be positive.")
    if vol < 0:
        raise ValueError("Volatility must be positive.")
    if option_type not in ["call", "put"]:
        raise ValueError("Option type must be 'call' or 'put'.")
    
    d1 = (np.log(S0/K)+(r+vol**2/2)*T)/(vol*np.sqrt(T))
    d2 = d1 - vol*np.sqrt(T)
    
    if option_type == "call":
        return S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    elif option_type == "put":
        return K*np.exp(-r*T)*norm.cdf(-d2)-S0*norm.cdf(-d1)
    
        
def delta_finder(S, K, r, tau, vol, option_type):
    """
    Compute the Black-Scholes delta for European call or put options (vectorised).
    
    Parameters
    ----------
    S : float or array-like
        Current asset price(s) in dollars. Can be a scalar or NumPy array.
    K : float
        Strike price of the option (must be positive).
    r : float
        Risk-free interest rate (annualised).
    tau : float or array-like
        Time(s) remaining to expiration, in years (non-negative).
    vol : float
        Volatility (annualised, must be positive).
    option_type : str
        Type of option: "call" or "put".
    
    Returns
    -------
    Delta : float or np.ndarray
        Option delta(s). Returns a float if inputs are scalar, or a NumPy array if inputs are vectorised.
    
    Raises
    ------
    ValueError
        If any input is invalid (e.g., negative prices, invalid option type).
    """
    S = np.atleast_1d(S).astype(float)
    tau = np.atleast_1d(tau).astype(float)
    K = float(K)


    # Input Checks
    if np.any(S < 0):
        raise ValueError("Asset price must be non-negative.")
    if K <= 0:
        raise ValueError("Strike price must be positive.")
    if np.any(tau < 0):
        raise ValueError("Time to expiration must be non-negative.")
    if vol < 0:
        raise ValueError("Volatility must be positive.")
    if option_type not in ["call", "put"]:
        raise ValueError("Option type must be 'call' or 'put'.")

    # Delta Computation
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * tau) / (vol * np.sqrt(tau))
        d1 = np.where(np.isclose(tau, 0), np.inf, d1)

    if option_type == "call":
        delta = norm.cdf(d1)
        delta = np.where(np.isclose(tau, 0), 1.0, delta)
    else:  
        delta = norm.cdf(d1) - 1
        delta = np.where(np.isclose(tau, 0), -1.0, delta)

    return delta

    
def gamma_finder(S, K, r, tau, vol, option_type):
    """
    Compute the Black-Scholes gamma for European call or put options (vectorised).
    
    Parameters
    ----------
    S : float or array-like
        Current asset price(s) in dollars. Can be a scalar or NumPy array.
    K : float
        Strike price of the option (must be positive).
    r : float
        Risk-free interest rate (annualised).
    tau : float or array-like
        Time(s) remaining to expiration, in years (non-negative).
    vol : float
        Volatility (annualised, must be positive).
    option_type : str
        Type of option: "call" or "put".
    
    Returns
    -------
    gamma : float or np.ndarray
        Option gamma(s). Returns a float if inputs are scalar, or a NumPy array if inputs are vectorised.
    
    Raises
    ------
    ValueError
        If any input is invalid (e.g., negative prices, invalid option type).
    """
    
    S = np.atleast_1d(S).astype(float)
    tau = np.atleast_1d(tau).astype(float)
    K = float(K)

    # Input Checks
    if np.any(S <= 0):
        raise ValueError("Asset price must be strictly positive.")
    if K <= 0:
        raise ValueError("Strike price must be positive.")
    if np.any(tau < 0):
        raise ValueError("Time to expiration must be non-negative.")
    if vol <= 0:
        raise ValueError("Volatility must be strictly positive.")
    if option_type not in ["call", "put"]:
        raise ValueError("Option type must be 'call' or 'put'.")

    # Gamma Computation
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * tau) / (vol * np.sqrt(tau))
        gamma = norm.pdf(d1) / (S * vol * np.sqrt(tau))
        gamma = np.where(np.isclose(tau, 0), 0.0, gamma)

    return gamma

        


    


    