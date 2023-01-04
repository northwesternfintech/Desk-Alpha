import time
import collections
import math
from numpy import inf


# This is the data structure for the stock's daily data; we will append each day's dictionary data to the self.data field (a list)
stock_data_day = {
  "Ticker": "APPL",
  "Opening Price": 100,
  "Closing Price": 200,
  "Lowest Price": 50,
  "Highest Price": 300,
  "Volume": 100000000
}

stocksdata = {
  "APPL": stock_data_day,
  "FISV": stock_data_day,
  #......#
}



class StochasticOscillator():
  """
  Relative strength strategies use the characteristics of the rest of the market or asset class to analyze a single stock. 
  The most famous example is the Relative Strength Index, which will be a future algorithm. For now, we will be using the Stochastic Oscillator 
  - a strategy that is designed to correspond with the over/under valuation of an asset - usually a high stochastic reading would indicate a sell, 
  and vice versa. It is up to you guys to test and implement those signals. Note that your trading sessions are completely up to you to decide. 
  """
  
  def __init__(self, stocksdata):
    """
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments. 
    """
    self.data = {} # Stores all the raw data for each stock in ticker (string) - single_stock_data (list of dictionaries) pairs
    self.time = time.time()
    self.orders = {} # Dictionary of ticker (string) - [buy/sell] (list of strings) pairs
    self.ticks = 0
    self.L14 = {} # Dictionary of ticker (string) - L14 (list) pairs
    self.H14 = {} # Dictionary of ticker (string) - H14 (list) pairs
    self.closing_price = {} # Dictionary of ticker (string) - price (float) pairs
  
def get_data(self):
  return self.data
def get_time(self):
  return self.time
def get_orders(self):
  return self.orders
def get_ticks(self):
  return self.ticks

def add_data(self, new_data):
  self.data.append(new_data)
def set_data(self, new_data):
  self.data = new_data
def set_time(self, new_time):
  self.time = new_time
def set_orders(self, new_orders):
  self.orders = new_orders
def set_ticks(self, new_tick):
  self.ticks = new_tickr



def clear_orders_stock(self, ticker):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d all orders", len(self.orders))
    self.orders[ticker] = []



def calculate_stochastic_oscillator(self, L14, H14, price):
    """
    Calculates RSI for a given stock given L14, H14, and price
    """
    K = (price - min(L14)) / (max(H14) - min(L14)) * 100
    return K
    


def update_stock(self, newdata):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    ""
    ticker = newdata["Ticker"]
    self.clear_orders_stock(ticker)
    self.data[ticker] = newdata

    # Update the lowest 14 price list
    self.L14[ticker].append(newdata["Lowest Price"])
    if len(self.L14[ticker]) > 14:
      self.L14[ticker].pop(0)
    
    # Update the highest 14 price list
    self.H14[ticker].append(newdata["Highest Price"])
    if len(self.H14[ticker]) > 14:
      self.H14[ticker].pop(0)

    # Update current price
    self.closing_price[ticker] = newdata["Closing Price"]

    K = calculate_stochastic_oscillator(self.L14[ticker], self.H14[ticker], newdata["Closing Price"])
    if K < 0.2:
      self.orders[ticker].append("BUY")
    elif K > 0.8:
      self.orders[ticker].append("SELL")



def update_all(self, newdata):
    """
    updates stock logic for all stocks.
    returns a dictionary of orders in the format {ticker : list_of_orders}
    """
    self.ticks += 1
    for ticker, stock_data in newdata:
      self.update_stock(stock_data)
    
    return self.orders







