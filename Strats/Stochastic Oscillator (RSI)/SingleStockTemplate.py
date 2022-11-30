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




class StochasticOscillator():
  """
  Relative strength strategies use the characteristics of the rest of the market or asset class to analyze a single stock. 
  The most famous example is the Relative Strength Index, which will be a future algorithm. For now, we will be using the Stochastic Oscillator 
  - a strategy that is designed to correspond with the over/under valuation of an asset - usually a high stochastic reading would indicate a sell, 
  and vice versa. It is up to you guys to test and implement those signals. Note that your trading sessions are completely up to you to decide. 
  """
  
  def __init__(self):
    """
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments. 
    """
    self.data = []
    self.time = time.time()
    self.orders = []
    self.ticks = 0
    self.trend = "downwards"
    self.L14 = []
    self.H14 = []
    self.stochastic_oscillator = 100
  
def get_data(self):
  return self.data
def get_time(self):
  return self.time
def get_orders(self):
  return self.orders
def get_ticks(self):
  return self.ticks
def get_trend(self):
  return self.trend

def add_data(self, new_data):
  self.data.append(new_data)
def set_data(self, new_data):
  self.data = new_data
def set_time(self, new_time):
  self.time = new_time
def set_orders(self, new_orders):
  self.orders = new_orders
def set_ticks(self, new_tick):
  self.ticks = new_tick
def set_trend(self, newTrend):
  self.trend = newTrend



def clear_orders(self):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d all orders", len(self.orders))
    self.orders = []
    


def update(self, newdata):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    """
    self.clear_orders()
    self.ticks += 1
    self.add_data(newdata)

    C = newdata["Closing Price"]

    self.L14.append(newdata["Losest Price"])
    if len(self.L14) > 14:
      self.L14.pop(0)
    
    self.H14.append(newdata["Highest Price"])
    if len(self.H14) > 14:
      self.H14.pop(0)

    L14 = min(self.L14)
    H14 = max(self.H14)

    self.stochastic_oscillator = (C - L14) / (H14 - L14) * 100

    if self.stochastic_oscillator < 0.2:
      self.orders.append("BUY")
    if self.stochastic_oscillator > 0.8:
      self.orders.append("SELL")

    return self.orders



