import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import Ss_gmr_strat

class Ms_gmr_strat:
    
    # Inputs: kwargs with lists of data
    # ** kwargs schema:
    # kwargs = {
    #     "tickers": ["AAPL"],    <- Lowercase only
    #     "data": [**kwargs],
    # }
    
    def __init__(self):
        
        # Inputs: **kwargs with a list of **kwargs
        self.ticker_data = {}
        self.decisions = {}
        
    
    
    ####################################################################
    # GETTER: Get the decisions of a particular ticker
    ####################################################################
    def get_decisions(self, ticker, option_type, strategy, gORv):
        
        gamma_decisions, vega_decisions = self.ticker_data[ticker].get_gamma_vega_decisions()
        
        if (gORv == "gamma"):
            return gamma_decisions[option_type][strategy]
        elif (gORv == "vega"):
            return vega_decisions[option_type][strategy]
        else:
            raise ValueError("gORv must be 'gamma' or 'vega'")
        
        
        
    ####################################################################
    # UPDATE: Update the tickers' decisions based on new data
    ####################################################################
    def update(self, **kwargs):
        
        list_of_tickers = list(kwargs.keys())
        
        # 1. Update ticker data
        # NOTE: When updating, it will update everythihng, which could potentially affect earlier decisions
        for ticker in list_of_tickers:
            
            # 2.1 Sanity check
            if kwargs[ticker] == {}: # empty dict
                raise ValueError("Empty dict for ticker: " + ticker)
            
            # 2.1. Check if ticker already exists
            if ticker not in self.ticker_data: 
                ss_obj = Ss_gmr_strat.Ss_gmr_strat() # initialize new object
                self.ticker_data[ticker] = ss_obj
                
            self.ticker_data[ticker].update(**kwargs[ticker])
        
        return "Success"
    
    
    
    ####################################################################
    # PLOTTING FUNCTION: Plot the gamma and vega decisions of a ticker
    ####################################################################
    def plotting_strat(self, ticker, option_type, strategy):
        
        ss_obj = self.ticker_data[ticker]
        ss_obj.plot_vega_gamma_decisions(option_type, strategy, ticker)
        