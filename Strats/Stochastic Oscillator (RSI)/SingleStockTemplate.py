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
    self.data = zip(metrics, initvalues)
    self.time = time.time()
    self.orders = []
    self.ticks = 0
    self.trend = "upwards"
#YOU WILL WANT A FULL SUITE OF SETTER AND GETTER METHODS!
  
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
    print(f"Trashing %d orders.", len(self.orders))
    self.orders = []
    


def update(self, data):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    """
    self.ticks += 1
    prev_price = self.data["price"]

    #Ingest Data
    updates = zip(data.keys(), data.values())

    for metric, information in updates:
      self.data[metric] = information
    self.clear_orders()

    #Re-run your logic
    if self.data['price'] > prev_price:
      if self.get_trend() == "downwards":
        self.orders.append('BUY')
        self.set_trend("upwards")

    elif self.data['price'] < prev_price:
      if self.get_trend() == "upwards":
        self.orders.append("SELL")
        self.set_trend("downwards")

    #More example logic
    return self.orders
    
