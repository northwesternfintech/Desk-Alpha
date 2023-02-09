import numpy as np
from scipy.stats import normal
import warnings

class QuantLib:
    def __init__(self):
        pass

    def variance(self, lst:list) -> float:
        """
        List variance calculator.
        - Inputs:
            - lst: list of real numbers (type = <class 'list'>)
        - Outputs:
            - variance of the list (type = <class 'float'>)
                - Note that if the list is empty, the function returns 0.
        """
        if lst is None or lst == []:
            return 0
        mu = 0
        for num in lst:
            if not isinstance(num, (int, float)):
                raise ValueError("Expected only real numbers in input list")
            mu += num
        mu = mu/len(lst)
        var = 0
        for num in lst:
            var += (num - mu)**2
        var = var/len(lst)
        return var
    
    def ma(self, type:str, data:list, period:int) -> tuple(list, float): 
        """
        Moving average calculation function.
        - Inputs:
            - type: 'ema' or 'sma' (type = <class 'str'>)
            - data: data (type = <class 'list'>)
            - period: period (type = <class 'int'>, >= 1)
        - Outputs:
            - return_lst: list of values after MA procedure (type = <class 'list'>)
                - Note that the first (period - 1) values are omitted.
            - last_value: last value of return_lst (type = <class 'float'>)
        """
        if len(data) < period:
            raise ValueError("Not enough data for calculation!")
        if period < 1:
            raise ValueError("Period must >= 1!")
        
        return_lst = []

        if type == 'ema':
            k = 2 / (period + 1)
            return_lst.append(sum(data[:period]) / period)
            for i in range(period, len(data)):
                return_lst.append(data[i] * k + return_lst[-1] * (1 - k))
        elif type == 'sma':
            for i in range(period, len(data)):
                return_lst.append(sum(data[i-period:i]) / period)
        else:
            raise TypeError("Invalid moving average type!")
        
        return return_lst, return_lst[-1]

    def BSM(self, type:str, spot:float, strike:float, risk_free:float, time:float, vol:float) -> float:
        """
        BSM pricing calculator.
        - Inputs:
            - type: 'call' or 'put' (type = <class 'str'>)
            - spot: spot price of the underlying asset (type = <class 'float'>)
            - strike: strike price of the option (type = <class 'float'>)
            - risk_free: risk-free interest rate (type = <class 'float'>)
            - time: time to maturity (type = <class 'float'>)
            - vol: implied volatility of the underlying asset (type = <class 'float'>)
        - Outputs:
            - calculated option price (type = <class 'float'>)
        """
        if spot <= 0 or strike <= 0 or time <= 0 or vol <= 0:
            raise ValueError("Invalid input value : spot price, strick price, time to maturity, or volatility must be positive!")

        if risk_free < 0:
            warnings.warn(f"Note: Entered Negative risk-free interest rate: {risk_free}")

        N = normal.cdf
        d1 = (np.log(spot/strike) + (risk_free + vol ** 2 / 2) * time) / vol * np.sqrt(time)
        d2 = d1 - vol * np.sqrt(time)

        if type == 'call':
            return spot * N(d1) - N(d2) * strike * np.exp(-risk_free * time)
        elif type == 'put':
            return N(-d2) * strike * np.exp(-risk_free * time) - N(-d1) * spot
        else:
            raise TypeError("Invalid option type!")