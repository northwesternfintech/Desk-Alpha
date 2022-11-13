import time
import collections
import math

#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.


class templateStrategy():
    """
  A base strategy that is used to explain how to properly develop a strategy.
  """

    def __init__(self, initDict):
        """
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    initDict - dictionary with tickers as keys, values are dictionaries where the keys are the metrics and the values are the initial values of your arguments.
    """
        self.data = initDict
        for ticker in initDict:
            ticker['trend'] = "Upward"
        self.time = time.time()
        self.orders = {}
        self.ticks = 0

    #YOU WILL WANT A FULL SUITE OF SETTER AND GETTER METHODS!
    def get_data(self):
        return self.data

    def get_time(self):
        return self.time

    def get_orders(self):
        return self.orders

    def get_ticks(self):
        return self.ticks

    def get_data_for_stock(self, ticker):
        return self.data[ticker]

    def set_data(self, data):
        self.data = data

    def set_time(self, time):
        self.time = time

    def set_orders(self, orders):
        self.orders = orders

    def set_ticks(self, ticks):
        self.ticks = ticks

    def set_data_for_stock(self, ticker, data):
        for metric in data:
            self.data[ticker][metric] = data[metric]

    def set_data(self, data):
        self.data = data

    def update_stock(self, ticker, data):
        """
        Updates the data for a given stock, and adds the order that should be made to the orders dict.
        @type ticker: str
        @type data: dict
        @rtype: None
        """
        prev_price = self.data[ticker]['price']
        prev_trend = self.data[ticker]['trend']
        self.set_data_for_stock(ticker, data);
        next_price = data['price']

        if(next_price > prev_price):
            if(prev_trend == "Downward"):
                self.orders[ticker] = "BUY"
            self.data[ticker]['trend'] = "Upward"

        elif(next_price < prev_price):
            if(prev_trend == "Upward"):
                self.orders[ticker] = "SELL"
            self.data[ticker]['trend'] = "Downward"

        else:
            self.orders[ticker] = "HOLD"

    def clear_orders(self):
        """
        Clears all current orders and logs relevant information.
        """
        print(f"Trashing %d orders.", len(self.orders))
        self.orders = {}


    def update(self, data):
        """
        Will be called on every tick to update the algorithm state and output buys/sells.
        @type data: dict
        @rtype: list
        """
        self.ticks += 1

        self.clear_orders()
        #Re-run your logic

        for stock in data:
            stock_data = data[stock]
            self.update_stock(stock, stock_data)

        return self.orders