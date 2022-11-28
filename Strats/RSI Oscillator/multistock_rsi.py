import time
import collections 
import math

class RSI_Oscillator():


    """
    Inputs required: 
        stock_data, a dictionary containing the following:

            L14: lowest price of the past 14 trading sessions
            H14: highest price of the past 14 trading sessions
            price: last closing price

    class variables:
        RSI
        price

    """

    
    def __init__(self, stock_data):
        self.data = {}
        self.orders = {}
        for ticker, data_dict in stock_data:
            self.data[ticker] = data_dict

            rsi = self.calculate_rsi(data_dict["L14"], data_dict["H14"], data_dict["price"])
            self.data[ticker]["rsi"] = rsi

            if rsi < 0.2:
                self.orders[ticker] = ["BUY"]
            elif rsi > 0.8:
                self.orders[ticker] = ["SELL"]

        self.ticks = 0
        self.time = time.time()



        
       
    

    #appropiate getters and setters
    def get_L14(self,ticker):
        return self.data[ticker]["L14"]
    
    def get_H14(self,ticker):
        return self.data[ticker]["H14"]
    
    def get_price(self, ticker):
        return self.data[ticker]["price"]

    def get_rsi(self, ticker):
        return self.data[ticker]["orders"]

    def get_orders(self, ticker):
        return self.orders[ticker]


    def set_L14(self, new_L14, ticker):
        self.data[ticker]["L14"] = new_L14

    def set_H14(self, new_H14, ticker):
        self.data[ticker]["H14"] = new_H14

    def set_price(self, new_price, ticker):
        self.data[ticker]["price"] = new_price

    def set_rsi(self, new_rsi, ticker):
        self.data[ticker]["rsi"] = new_rsi

    def set_orders(self, new_orders, ticker):
        self.orders[ticker] = new_orders




    #returns a value from 0-1 representing the RSI
    def calculate_rsi(self, L14, H14, price):
        rsi = (price-L14)/(H14-L14)
        return rsi



    def clear_orders_stock(self, ticker):
        """
        Clears all current orders and logs relevant information.
        """
        print(f"Trashing %d orders.", len(self.orders))
        self.orders[ticker] = []
        

    
        

    def update_stock(self, ticker):
        self.clear_orders_stock(ticker)
        ticker_data = self.data[ticker]

        rsi = self.calculate_rsi(ticker_data["L14"], ticker_data["H14"], ticker_data["price"])
        if rsi < 0.2:
            self.orders[ticker].append("BUY")
        elif rsi > 0.8:
            self.orders[ticker].append("SELL")
        


    def update(self, data):
        self.ticks += 1
        for ticker, ticker_data in data:
            self.data[ticker] = ticker_data
            self.update_stock(ticker) 
        
        return self.orders


    
    