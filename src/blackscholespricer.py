import numpy as np
from scipy.stats import norm

def BS_optionprice(S0, K, r, T, vol, option_type):
    """
    Black-Scholes Option Valuation.

    Parameters
    ----------
    S0 : float
        Initial asset price (must be non-negative).
    K : float
        Strike price (must be positive).
    r : float
        Risk-free interest rate (annualised, as a decimal).
    T : float
        Time to expiration in years (must be non-negative).
    vol : float
        Annualised volatility (must be positive).
    option_type : str
        Option type ("call" or "put").

    Returns
    -------
    float
        Option price (call or put) in dollars.
    """

    # Input Validation
    
    if S0 < 0:
        raise ValueError("Initial asset price must be non-negative.")
    if K <= 0:
        raise ValueError("Strike price must be positive.")
    if T < 0:
        raise ValueError("Time to expiration must be non-negative.")
    if vol < 0:
        raise ValueError("Volatility must be positive.")
    if option_type not in ["call", "put"]:
        raise ValueError("Option type must be 'call' or 'put'.")

    # Expiry Check
    
    if np.isclose(T, 0):
        return max(S0 - K, 0) if option_type == "call" else max(K - S0, 0)

    # Black-Scholes Formulae
    
    d1 = (np.log(S0 / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)

    if option_type == "call":
        return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # Put
        return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)


def delta_finder(S, K, r, tau, vol, option_type):
    """
    Compute Black-Scholes Delta for European options.

    Parameters
    ----------
    S : float or array-like
        Current asset price(s).
    K : float
        Strike price (must be positive).
    r : float
        Risk-free interest rate (annualised).
    tau : float or array-like
        Time(s) remaining to expiration in years (non-negative).
    vol : float
        Annualised volatility (must be positive).
    option_type : str
        Option type ("call" or "put").

    Returns
    -------
    float or np.ndarray
        Delta(s) for the option.
    """

    tau = np.atleast_1d(tau).astype(float)
    S = np.atleast_1d(S).astype(float)

    # Input Validations
    
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

    # Delta Calculation
    
    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * tau) / (vol * np.sqrt(tau))
        d1 = np.where(np.isclose(tau, 0), np.inf, d1)

    if option_type == "call":
        delta = norm.cdf(d1)
        delta = np.where(np.isclose(tau, 0), 1.0, delta)
    else: # Put
        delta = norm.cdf(d1) - 1.0
        delta = np.where(np.isclose(tau, 0), -1.0, delta)

    return delta


def gamma_finder(S, K, r, tau, vol, option_type):
    """
    Compute Black-Scholes gamma for European options.

    Parameters
    ----------
    S : float or array-like
        Current asset price(s).
    K : float
        Strike price (must be positive).
    r : float
        Risk-free interest rate (annualised).
    tau : float or array-like
        Time(s) remaining to expiration in years (non-negative).
    vol : float
        Annualised volatility (must be positive).
    option_type : str
        Option type ("call" or "put").

    Returns
    -------
    float or np.ndarray
        Gamma(s) for the option.
    """
    
    S = np.atleast_1d(S).astype(float)
    tau = np.atleast_1d(tau).astype(float)

    # Input Validations    

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

    # Gamma Calculation

    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = (np.log(S / K) + (r + 0.5 * vol**2) * tau) / (vol * np.sqrt(tau))
        gamma = norm.pdf(d1) / (S * vol * np.sqrt(tau))
        gamma = np.where(np.isclose(tau, 0), 0.0, gamma)

    return gamma

