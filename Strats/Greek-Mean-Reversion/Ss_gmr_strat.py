import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

class Ss_gmr_strat():
    
    # Inputs: kwargs with lists of data
    # ** kwargs schema:
    # kwargs = {
    #     "option_strategy": ["long/short"],    <- Lowercase only
    #     "option_type": ["call/put"],          <- Lowercase only
    #     "strikes": [100],
    #     "underlying_price": [100]
    #     "option_price": [10],
    #     "interest_rate": [0.05],
    #     "dividend_yields": [0],               <- Must be annual dividend yield
    #     "time_to_expiration": [1],            <- Store in seconds/minutes, not a datetime object
    #     "implied_volatility": [0.56],         <- list as well
    # }
    
    
    
    
    # 1. Call Option Type
    # 2. Black Scholes Inputs: Strike, Underlying Price, Option Price, Interest Rates, Dividends, Time Until Expiration
    
    def __init__(self):
        
        self.emptykwargs = {
            "option_strategy": [], 
            "option_type": [],     
            "strikes": [],
            "underlying_price": [],
            "option_price": [],
            "interest_rate": [],
            "dividend_yields": [],              
            "time_to_expiration": [],         
            "implied_volatility": [],      
        }
        
        self.data_short_call = {}
        self.data_long_call = {}
        self.data_short_put = {}
        self.data_long_put = {}
        self.data_update(**self.emptykwargs) # initiate the data
        
        self.gamma = {"call":{"short":[], "long":[]}, "put":{"short":[], "long":[]}} # option type -> option strategy -> gamma
        self.vega = {"call":{"short":[], "long":[]}, "put":{"short":[], "long":[]}} # option type -> option strategy -> vega
        self.tte = {"call":{"short":[], "long":[]}, "put":{"short":[], "long":[]}} # option type -> option strategy -> time to expiration
        
        self.gamma_regression = {"call":{"short":{"intercept":0, "slope":0}, "long":{"intercept":0, "slope":0}}, "put":{"short":{"intercept":0, "slope":0}, "long":{"intercept":0, "slope":0}}}  # option type -> option strategy -> {"intercept":0, "slope":0}
        self.vega_regression = {"call":{"short":{"intercept":0, "slope":0}, "long":{"intercept":0, "slope":0}}, "put":{"short":{"intercept":0, "slope":0}, "long":{"intercept":0, "slope":0}}}  # option type -> option strategy -> {"intercept":0, "slope":0}
        
        self.gamma_decisions = {"call":{"short":[], "long":[]}, "put":{"short":[], "long":[]}} # option type -> option strategy -> {time: [buy, sell, hold]}
        self.vega_decisions = {"call":{"short":[], "long":[]}, "put":{"short":[], "long":[]}} # option type -> option strategy -> {time: [buy, sell, hold]}
        self.combined_decisions = {"call":{"short":[], "long":[]}, "put":{"short":[], "long":[]}} # option type -> option strategy -> {time: [buy, sell, hold]} NOT SURE IF NEEEDED, NOT YET IMPLEMENTED
    
        
    ####################################################################
    # HELPER for data_init: very inefficient storying as dictionary, but should be intuitive for testing at least
    # NOTE: will always overwrite existing data
    ####################################################################
    def data_update(self, **kwargs):
        for i in range(len(kwargs["time_to_expiration"])):
            
            item_to_add = { "strikes": kwargs["strikes"][i], \
                            "underlying_price": kwargs["underlying_price"][i], \
                            "option_price": kwargs["option_price"][i], \
                            "interest_rate": kwargs["interest_rate"][i], \
                            "dividend_yields": kwargs["dividend_yields"][i], \
                            "time_to_expiration": kwargs["time_to_expiration"][i], \
                            "implied_volatility": kwargs["implied_volatility"][i]}
            
            option_type = kwargs["option_type"][i]
            option_strategy = kwargs["option_strategy"][i]
            tte = kwargs["time_to_expiration"][i]
            
            if option_strategy == "long" and option_type == "call":
                self.data_long_call[tte] = item_to_add
            elif option_strategy == "short" and option_type == "call":
                self.data_short_call[tte] = item_to_add
            elif option_strategy == "long" and option_type == "put":
                self.data_long_put[tte] = item_to_add
            elif option_strategy == "short" and option_type == "put":
                self.data_short_put[tte] = item_to_add
                
            self.tte[option_type][option_strategy].append(tte)
    
    ####################################################################
    # HELPER for Choosing the right data set
    ####################################################################      
            
    def choose_ls(self, strat, option_type):
        
        ls = {}
        
        if strat == "long" and option_type == "call":
            ls = self.data_long_call
        elif strat == "short" and option_type == "call":
            ls = self.data_short_call
        elif strat == "long" and option_type == "put":
            ls = self.data_long_put
        elif strat == "short" and option_type == "put":
            ls = self.data_short_put
        
        return ls
            
            
    ####################################################################
    # HELPER for Data-Cleaning: Filter options that are not in the money
    ####################################################################
    def filter_in_the_money(self, strat, option_type):
        
        ls = self.choose_ls(strat, option_type) # the data dictionary we are going to use
        tte = self.tte[option_type][strat] # the time to expiration list we are going to use
        
        to_remove = []
        
        # for loop for cleaning
        for i in tte:
            if strat == "long" and option_type == "call":
                if ls[i]["underlying_price"] < ls[i]["strikes"]:
                    to_remove.append(i)
            elif strat == "short" and option_type == "call":
                if ls[i]["underlying_price"] > ls[i]["strikes"]:
                    to_remove.append(i)
            elif strat == "long" and option_type == "put":
                if ls[i]["underlying_price"] > ls[i]["strikes"]:
                    to_remove.append(i)
            elif strat == "short" and option_type == "put":
                if ls[i]["underlying_price"] < ls[i]["strikes"]:
                    to_remove.append(i)
            else:
                return "Error: Invalid option strategy or option type"
            
        # deleting the dictionary to avoid manipulating the length during the operations
        for key in to_remove:
            del ls[key]
            
        # removing the items from the tte list
        for key in to_remove:
            tte.remove(key)
            
        return ls
        
        
    
        
    ####################################################################
    # HELPER for VEGA: Find d1
    ####################################################################
    def helper_vega_d1(self, stock_price, strike, risk_free_rate, dividend_yield, implied_volatility, time_to_expiration):
        return (math.log(stock_price/strike) + (risk_free_rate - dividend_yield + implied_volatility * implied_volatility/2)*time_to_expiration)/(implied_volatility*math.sqrt(time_to_expiration))
    
    
    ####################################################################
    # HELPER for VEGA: Find d2
    ####################################################################
    def helper_vega_d2(self, stock_price, strike, risk_free_rate, dividend_yield, implied_volatility, time_to_expiration):
        return (math.log(stock_price/strike) + (risk_free_rate - dividend_yield - implied_volatility * implied_volatility/2)*time_to_expiration)/(implied_volatility*math.sqrt(time_to_expiration))
    
    
    ####################################################################
    # HELPER for Phi: Find phi, input: d2, Phi(x)
    ####################################################################
    def helper_vega_phi(self, x):
        return math.exp(-(x*x)/2)/math.sqrt(2*math.pi)
    
    
    ####################################################################
    # HELPER for Sorting self.data by time to expiration
    ####################################################################
    def sort_self_data(self, strat, option_type):
        
        ls = self.choose_ls(strat, option_type)
        
        # sort the values
        myKeys = list(ls.keys())
        myKeys.sort()
        sorted_dict = {i: ls[i] for i in myKeys}
        
        # sort the time to expiration
        self.tte[option_type][strat].sort()
        
        return sorted_dict
    
    
    ####################################################################
    # HELPER: Find the delta of the given data set
    ####################################################################    
    def calculate_delta(self, strat, option_type):
        
        delta_arr = []
        data = self.choose_ls(strat, option_type)
        data_keys = list(data.keys())
        
        # find delta using python loop, they are all in order already by logic of update
        for i in range(len(data_keys) - 1):
            
            key = data_keys[i]
            later_key = data_keys[i + 1]
            
            option_price_0 = data[key]["option_price"]
            underlying_price_0 = data[key]["underlying_price"]
            option_price_1 = data[later_key]["option_price"]
            underlying_price_1 = data[later_key]["underlying_price"]
            
            # case of 0 division
            if underlying_price_1 - underlying_price_0 == 0:
                delta_arr.append(0) # for 0 change in underlying price, we show gap
                continue
            delta_arr.append((option_price_1 - option_price_0) / (underlying_price_1 - underlying_price_0))
            
            
        return delta_arr
    
    
    ####################################################################
    # HELPER: Find the gamma of the given dataset
    ####################################################################
    def calculate_gamma(self, strat, option_type):
        delta_arr = self.calculate_delta(strat, option_type)
        gamma_arr = []
        data = self.choose_ls(strat, option_type)
        
        data_keys = list(data.keys())
        
        # they are all in order already by logic of update
        for i in range(len(delta_arr)-1):
            
            key = data_keys[i + 1]
            later_key = data_keys[i + 2]
            
            delta_0 = delta_arr[i]
            underlying_price_0 = data[key]["underlying_price"]
            delta_1 = delta_arr[i + 1]
            underlying_price_1 = data[later_key]["underlying_price"]
            
            if underlying_price_1 - underlying_price_0 == 0 or delta_1 - delta_0 == 0:
                gamma_arr.append(0) # need to optimize this
                continue
            
            gamma_arr.append((delta_1 - delta_0) / (underlying_price_1 - underlying_price_0))
            
        return gamma_arr
    
    
    ####################################################################
    # HELPER: Find the vega value of the given data
    ####################################################################
    
    def calculate_vega(self, strat, option_type):
        
        vega_arr = []
        
        data = self.choose_ls(strat, option_type)
        data_keys = list(data.keys())
            
        for i in range(len(data)):
            
            tte = data_keys[i]
            up = data[tte]["underlying_price"]
            strike = data[tte]["strikes"]
            ir = data[tte]["interest_rate"]
            div_yields = data[tte]["dividend_yields"]
            sigma = data[tte]["implied_volatility"]

            # Can use d1 method as well
            # d1 = self.helper_vega_d1(up, strike, ir, div_yields, sigma, tte)
            # phi = self.helper_vega_phi(d1)
            # vega = up * math.exp(-div_yields * tte) * phi * math.sqrt(tte)
            
            d2 = self.helper_vega_d2(up, strike, ir, div_yields, sigma, tte)
            phi = self.helper_vega_phi(d2)
            vega = strike * math.exp(-ir * tte) * phi * math.sqrt(tte)
            
            vega_arr.append(vega)
            
        return vega_arr           
    
    
    ####################################################################
    # UPDATE: Find the stock decisions
    ####################################################################
    
    # implementation of the Greek Mean-Reversion Strategy
    def update(self, **kwargs):
        
        # 0.5 Check types
        option_strategy = kwargs["option_strategy"]
        option_types = kwargs["option_type"]
        eval_zip = []
        
        for i in range(len(option_types)):
            if option_types[i] == "call":
                if option_strategy[i] == "long" and ("call", "long") not in eval_zip:
                    eval_zip.append(("call", "long"))
                elif option_strategy[i] == "short" and ("call", "short") not in eval_zip:
                    eval_zip.append(("call", "short"))
            elif option_types[i] == "put":
                if option_strategy[i] == "long" and ("put", "long") not in eval_zip:
                    eval_zip.append(("put", "long"))
                elif option_strategy[i] == "short" and ("put", "short") not in eval_zip:
                    eval_zip.append(("put", "short"))
                    
        # now we go through all the option types and strategies that have seen changes
    
        # 1 Update self.data
        self.data_update(**kwargs)
        
        # now we start the loop to go through everything
        for item in eval_zip:
            
            print("Evaluating: ", item[0], item[1], " options")
            
            option_type_selected = item[0]
            option_strategy_selected = item[1]
            
            # 1.5 Filter the in the money options + Data Sorting
            self.sort_self_data(option_strategy_selected, option_type_selected) # sort the data by time to expiration
            self.filter_in_the_money(option_strategy_selected, option_type_selected)
            
            
            # 2. Calculate the Greeks, everything is accessed through self.data
            self.gamma[option_type_selected][option_strategy_selected] = self.calculate_gamma(option_strategy_selected, option_type_selected) # re-calculate, not optimized
            self.vega[option_type_selected][option_strategy_selected] = self.calculate_vega(option_strategy_selected, option_type_selected) # re-calculate, not optimized
            tte = self.tte[option_type_selected][option_strategy_selected]
            mod_tte = tte[2:]
            
            
            # 3. Regressions, might include previous data
            # First, we determine the regression line for each greek
            gamma = np.array(self.gamma[option_type_selected][option_strategy_selected])
            vega = np.array(self.vega[option_type_selected][option_strategy_selected])
            tte = np.array(tte)
            mod_tte = np.array(mod_tte)
            
            y_gamma = LinearRegression().fit(mod_tte.reshape(-1,1), gamma.reshape(-1,1))
            y_vega = LinearRegression().fit(tte.reshape(-1,1), vega.reshape(-1,1))
            
            self.gamma_regression[option_type_selected][option_strategy_selected]["intercept"] = y_gamma.intercept_
            self.gamma_regression[option_type_selected][option_strategy_selected]["slope"] = y_gamma.coef_[0]
            
            self.vega_regression[option_type_selected][option_strategy_selected]["intercept"] = y_vega.intercept_
            self.vega_regression[option_type_selected][option_strategy_selected]["slope"] = y_vega.coef_[0]
            
            
            # 5. Determine the stock decision, might include previous data
            # vega has one more item than gamma, so we need to evaluate the first element
            val = self.vega_regression[option_type_selected][option_strategy_selected]["intercept"] + self.vega_regression[option_type_selected][option_strategy_selected]["slope"] * tte[0]
            
            if vega[0] > val:
                self.vega_decisions[option_type_selected][option_strategy_selected].append("Buy")
            elif vega[0] < val:
                self.vega_decisions[option_type_selected][option_strategy_selected].append("Sell")
            else:
                self.vega_decisions[option_type_selected][option_strategy_selected].append("Hold")    
            
            for i in range(0, len(gamma)):
                
                vega_ind = i + 1
                
                gamma_reg = self.vega_regression[option_type_selected][option_strategy_selected]["intercept"] + self.vega_regression[option_type_selected][option_strategy_selected]["slope"] * tte[i]
                vega_reg = self.vega_regression[option_type_selected][option_strategy_selected]["intercept"] + self.vega_regression[option_type_selected][option_strategy_selected]["slope"] * tte[vega_ind]
                
                # evaluate gamma first
                if gamma[i] > gamma_reg:
                    self.gamma_decisions[option_type_selected][option_strategy_selected].append({tte[i]: "Buy"})
                elif gamma[i] < gamma_reg:
                    self.gamma_decisions[option_type_selected][option_strategy_selected].append({tte[i]: "Sell"})
                else:
                    self.gamma_decisions[option_type_selected][option_strategy_selected].append({tte[i]: "Hold"})
                
                # evaluate vega
                if vega[vega_ind] > vega_reg:
                    self.vega_decisions[option_type_selected][option_strategy_selected].append({tte[vega_ind]: "Buy"})
                elif vega[vega_ind] < vega_reg:
                    self.vega_decisions[option_type_selected][option_strategy_selected].append({tte[vega_ind]: "Sell"})
                else:
                    self.vega_decisions[option_type_selected][option_strategy_selected].append({tte[vega_ind]: "Hold"})
                
        return self.gamma_decisions, self.vega_decisions
            
    ####################################################################
    # GETTER: Get the decisions
    ####################################################################     
    def get_gamma_vega_decisions(self):
        return self.gamma_decisions, self.vega_decisions
            
    ####################################################################
    # GETTER: Get the parsed data
    ####################################################################   
    def get_data(self):
        return self.data_short_call, self.data_short_put, self.data_long_call, self.data_long_put
    
    
    ####################################################################
    # PLOTTER: Plot a specific option strategy
    ####################################################################     
    def plot_vega_gamma_decisions(self, option_type_selected, option_strategy_selected, ticker_title):
        
        # sanity checks
        if self.tte[option_type_selected][option_strategy_selected] == []:
            raise ValueError("No data available for this option strategy")
        
        tte_gamma = self.tte[option_type_selected][option_strategy_selected][2:]
        tte_vega = self.tte[option_type_selected][option_strategy_selected]
        data_gamma = self.gamma[option_type_selected][option_strategy_selected]
        data_vega = self.vega[option_type_selected][option_strategy_selected]
        
        print("debug test: ", self.gamma_regression[option_type_selected][option_strategy_selected]["intercept"], self.gamma_regression[option_type_selected][option_strategy_selected]["slope"], tte_gamma)
        print("debug test 2: ", self.gamma_regression[option_type_selected][option_strategy_selected]["slope"] * tte_gamma)
        reg_gamma = self.gamma_regression[option_type_selected][option_strategy_selected]["intercept"] + self.gamma_regression[option_type_selected][option_strategy_selected]["slope"] * tte_gamma
        reg_vaga = self.vega_regression[option_type_selected][option_strategy_selected]["intercept"] + self.vega_regression[option_type_selected][option_strategy_selected]["slope"] * tte_vega
        
        plt.figure(1)
        plt.plot(tte_gamma, data_gamma, label="Gamma Vs. Time to Expiration")
        plt.plot(tte_gamma, reg_gamma, label="Regression Line")
        plt.xlabel("Time to Expiration")
        plt.ylabel("Gamma")
        plt.title("Gamma Vs. Time to Expiration for " + option_strategy_selected + " " + option_type_selected + " on " + ticker_title)
        plt.figure(2)
        plt.plot(tte_vega, data_vega, label="Vega Vs. Time to Expiration")
        plt.plot(tte_vega, reg_vaga, label="Regression Line")
        plt.xlabel("Time to Expiration")
        plt.ylabel("Vega")
        plt.title("Vega Vs. Time to Expiration for " + option_strategy_selected + " " + option_type_selected + " on " + ticker_title)
        plt.show()
    
        
        
        
        
        
        
        
        
    