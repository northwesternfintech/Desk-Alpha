import time
import collections
import math
from collections import defaultdict

#Single-stock template for EMA strategy

class EMAMultiStock():
  """
  Multi-stock template for overlapping EMA strategy
  """
  
  def __init__(self, allStockTickers):
    """
    Version of init if we have no previous data
    @type allStockTickers: list
    """
    self.data = defaultdict({})
    for stock in allStockTickers:
      self.data[stock]["price"] = 0
      self.data[stock]["time"] = time.time()
      self.data[stock]["EMA200d"] = 0
      self.data[stock]["EMA50d"] = 0
      self.data[stock]["days"] = 0
      self.data[stock]["shortOverLong"] = False
    self.orders = {}
    
  def set_price(self,ticker,newPrice):
    self.data[ticker]["price"] = newPrice

  def set_time(self,ticker,newTime):
    self.data[ticker]["time"] = newTime

  def set_ticks(self,ticker,newTicks):
    self.data[ticker]["ticks"] = newTicks

  def set_EMA50d(self,ticker,newEMA50d):
    self.data[ticker]["EMA50d"] = newEMA50d

  def set_EMA50d(self,ticker,newEMA200d):
    self.data[ticker]["EMA200d"] = newEMA200d

  def set_days(self,ticker,newDays):
    self.data[ticker]["days"] = newDays

  def get_price(self,ticker):
    return self.data[ticker]["price"]

  def get_time(self,ticker):
    return self.data[ticker]["time"]

  def get_ticks(self,ticker):
    return self.data[ticker]["ticks"]

  def get_EMA50d(self,ticker):
    return self.data[ticker]["EMA50d"]

  def get_EMA50d(self,ticker):
    return self.data[ticker]["EMA200d"]

  def get_days(self,ticker):
    return self.data[ticker]["days"]
  
  def clear_orders(self):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d orders.", len(self.orders))
    self.orders = {}

  def calculate_ema(days, newPrice, prev_ema):
    """
    @type days: int
    @type newPrice: float
    @type prev_ema: float
    @rtype: float
    """
    mult = 2/(days+1)
    new_ema = newPrice*mult + prev_ema*(1-mult)
    return new_ema
    
  def update(self, **kwargs):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    kwargs should be a dict with keys being tickers and values being the associated new price
    @type kwargs: dict
    @rtype: dict
    """
    self.clear_orders()
    for ticker in kwargs:
      newPrice = kwargs[ticker]
      self.data[ticker]["days"] += 1
      days = self.data[ticker]["days"]
      if self.data[ticker]["days"]<50:
        self.data[ticker]["EMA50d"] = self.calculate_ema(days, newPrice, self.data[ticker]["EMA50d"])
        self.data[ticker]["EMA200d"] = self.calculate_ema(days, newPrice, self.data[ticker]["EMA200d"])
      elif self.data[ticker]["days"]<200:
        self.data[ticker]["EMA50d"] = self.calculate_ema(50, newPrice, self.data[ticker]["EMA50d"])
        self.data[ticker]["EMA200d"] = self.calculate_ema(days, newPrice, self.data[ticker]["EMA200d"])
      else:
        self.data[ticker]["EMA50d"] = self.calculate_ema(50, newPrice, self.data[ticker]["EMA50d"])
        self.data[ticker]["EMA200d"] = self.calculate_ema(200, newPrice, self.data[ticker]["EMA200d"])

      if self.data[ticker]["EMA50d"]>self.data[ticker]["EMA200d"]: 
        if not(self.data[ticker]["shortOverLong"]) and self.data[ticker]["days"]>250: #Buy when short signal rises above long signal
          self.orders[ticker] = "BUY"               
        self.data[ticker]["shortOverLong"] = True
      elif self.data[ticker]["EMA50"]<=self.data[ticker]["EMA200d"]: 
        if self.data[ticker]["shortOverLong"] and self.data[ticker]["days"]>250: #Sell when short signal dips below long signal
          self.orders[ticker] = "SELL"                   
        self.data[ticker]["shortOverLong"] = False

    return self.orders
