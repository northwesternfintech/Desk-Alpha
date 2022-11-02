import time
import collections
import math

#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.

class templateStrategy():
  """
  A base strategy that is used to explain how to properly develop a strategy.
  """
  
  def __init__(self, initData):
    """
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments. 
    """
    #initData: dict w key = ticker, value = dict mapping metric to data
    self.data = {}
    self.orders = {}
    self.trends = {}
    for ticker, dataDict in initData.items():
      self.data[ticker] = dataDict
      self.orders[ticker] = []
      self.trends[ticker] = "Upward"
    self.time = time.time()
    self.ticks = 0
  
  #YOU WILL WANT A FULL SUITE OF SETTER AND GETTER METHODS!
  def get_data(self, ticker):
    return self.data[ticker]
  def get_time(self):
    return self.time
  def get_orders(self, ticker):
    return self.orders[ticker]
  def get_ticks(self):
    return self.ticks
  def get_trend(self, ticker):
    return self.trend[ticker]
  def set_trend(self, ticker, newTrend):
    self.trends[ticker] = newTrend
    
  
def clear_orders(self, ticker):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d orders.", len(self.orders[ticker]))
    self.orders[ticker] = []
#generic update method that calls update on every ticker
def update_all(self, ticker):
    for ticker in self.data:
        self.data[ticker] = self.update(ticker, self.data[ticker])

def update(self, ticker, data):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    @type data: dict
    @rtype: list
    """
    self.ticks += 1
    previousPrice = data['price']

    #Ingest Data
    updates = zip(data.keys(), data.values())

    for metric, information in updates:
      self.data[metric] = information
      
    self.clear_orders(ticker)
    #Re-run your logic

    if data['price'] > previousPrice: #if price is greater than last
      if self.get_trend(ticker) == "Downward":  #if stock was previously going down
        self.orders[ticker].append('BUY') #buy the stock
      self.set_trend(ticker, "Upward") #set new trend to upward
      

    elif data['price'] < previousPrice: #if price is lower than last
      if self.get_trend(ticker) == "Upward": #if stock was previously going up
        self.orders.append('SELL') #sell the stock
      self.set_trend(ticker, "Downward") #set new trend to downward
    
    #More example logic
    return self.orders
