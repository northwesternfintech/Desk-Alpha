import time
import collections
import math

#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.

class templateStrategy():
  """
  A base strategy that is used to explain how to properly develop a strategy.
  """
  
  def __init__(self, stocksdata):
    """
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments. 
    """
    """
    In the multiple stock case, we take in a dictionary of stock data "stocksdata": {ticker: {data dict}};
    Initialize all stock's "trend" field to "downwards" so we buy the stock whenever the price goes up for the first time.
    """
    self.data = stocksdata
    for stock in stocksdata:
      stock["trend"] = "downwards"
    self.time = time.time()
    self.orders = dict()
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
def get_stock_data(self, ticker):
  return self[ticker]

def set_data(self, new_data):
  self.data = new_data
def set_time(self, new_time):
  self.time = new_time
def set_orders(self, new_orders):
  self.orders = new_orders
def set_ticks(self, new_tick):
  self.ticks = new_tick
def set_stock_data(self, ticker, single_stock_data):
  for metric in single_stock_data:
    self[ticker][metric] = single_stock_data[metric]



def clear_orders(self):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d orders.", len(self.orders))
    self.orders = []
  


def update_stock(self, ticker, data):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    """
    #Ingest Data
    prev_price = self.data[ticker]["price"]
    prev_trend = self.data[ticker]["trend"]
    self.set_stock_data(ticker, data)
    curr_price = self.data[ticker]["price"]

    #Re-run your logic
    if curr_price > prev_price:
      if prev_trend == "downwards":
        self.orders[ticker].append('BUY')
        self.data[ticker]["trend"] = "upwards"

    elif curr_price < prev_price:
      if prev_trend == "upwards":
        self.orders[ticker].append("SELL")
        self.data[ticker]["trend"] = "downwards"



def update_all(self, new_stocksdata):
    self.clear_orders()
    self.ticks += 1

    for ticker in new_stocksdata:
      stock_data = new_stocksdata[ticker]
      self.update_stock(ticker, stock_data)

    #More example logic
    return self.orders
    
