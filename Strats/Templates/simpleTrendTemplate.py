import time
import collections
import math

#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.

class templateStrategy():
  """
  A base strategy that is used to explain how to properly develop a strategy.
  """
  
  def __init__(self, metrics, initvalues):
    """
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments. 
    """
    self.data = zip(metrics,initvalues)
    self.time = time.time()
    self.orders = []
    self.ticks = 0
    self.upwardTrend = False
  
  #YOU WILL WANT A FULL SUITE OF SETTER AND GETTER METHODS!
  def get_data(self):
    return self.orders
  def get_time(self):
    return self.time
  def get_orders(self):
    return self.orders
  def get_ticks(self):
    return self.ticks
  def upward_Trending(self):
    return self.upwardTrend
    
  
def clear_orders(self):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d orders.", len(self.orders))
    self.orders = []
    
def update(self, data):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    @type data: dict
    @rtype: list
    """
    self.ticks += 1
    previousPrice = self.data['price']

    #Ingest Data
    updates = zip(data.keys(), data.values())

    for metric, information in updates:
      self.data[metric] = information
      
    self.clear_orders()
    #Re-run your logic

    if self.data['price'] > previousPrice: #if price is greater than last
      if not self.upward_Trending():  #if stock was previously going down
        self.orders.append('BUY') #buy the stock
        
    elif self.data['price'] < previousPrice: #if price is lower than last
      if self.upward_Trending(): #if stock was previously going up
        self.orders.append('SELL') #sell the stock
    
    #More example logic
    return self.orders
    