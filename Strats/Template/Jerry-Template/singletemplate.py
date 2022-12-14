

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
#YOU WILL WANT A FULL SUITE OF SETTER AND GETTER METHODS!
def get_data(self, metric):
    """
    Returns the data for a given metric.
    """
    return self.data[metric]

def set_data(self, metric, value):
    """
    Sets the value of a metric.
    """
    self.data[metric] = value

def get_time(self):
    """
    Returns the time since the last update.
    """
    return self.time

def set_time(self, time):
    """
    Sets the time since the last update.
    """
    self.time = time

def get_ticks(self):
    """
    Returns the number of ticks that have passed.
    """
    return self.ticks

def set_ticks(self, ticks):
    """
    Sets the number of ticks that have passed.
    """
    self.ticks = ticks

def get_orders(self):
    """
    Returns the current orders.
    """
    return self.orders

def set_orders(self, orders):
    """
    Sets the orders to be executed.
    """
    self.orders = orders


  
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
    #Ingest Data
    updates = zip(data.keys(), data.values())
    for metric, information in updates:
      self.data[metric] = information
      
    self.clear_orders()
    if self.data['50_day_moving_average'] > self.data['200_day_moving_average']:
        self.orders.append('BUY')
    if self.data['50_day_moving_average'] < self.data['200_day_moving_average']:
        self.orders.append('SELL')
    # if self.data['price'] > 100:
    #   self.orders.append('BUY')
    #More example logic
    return self.orders