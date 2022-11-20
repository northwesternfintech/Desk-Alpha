import time
import collections
import math

#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.

class templateStrategy():
  """
  A base strategy that is used to explain how to properly develop a strategy.
  """
  
  def __init__(self, price):
    """
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments. 
    """
    self.price = 0
    self.time = time.time()
    self.order = []
    self.ticks = 0
    self.EMA200d = 0
    self.EMA50d = 0
    self.days = 0
  
  #YOU WILL WANT A FULL SUITE OF SETTER AND GETTER METHODS!
  def get_price(self):
    return self.price
  def get_time(self):
    return self.time
  def get_orders(self):
    return self.orders
  def get_ticks(self):
    return self.ticks
  def get_EMA50(self):
    return self.EMA50d
  def get_EMA200(self):
    return self.EMA200d
  def get_days(self):
    return self.days
    
  
def clear_orders(self):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d orders.", len(self.orders))
    self.orders = []
    
def update(self, newPrice):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    @type data: dict
    @rtype: list
    """
    self.ticks += 1
      
    self.clear_orders()
    #Re-run your logic

    
    
    #More example logic
    return self.orders
    