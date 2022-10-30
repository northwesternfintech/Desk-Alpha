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

    def get_data():
        return self.data
    def get_time():
        return self.time
    def get_orders():
        return self.orders
    def get_ticks():
        return self.ticks


    def set_data(d):
        self.data = d
    def set_time(t):
        self.time = t
    def set_orders(o):
        self.orders = o
    def set_ticks(t):
        self.ticks = t

  
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
    #Re-run your logic
    if self.data['price'] > self.data['previous price']:
        self.orders.append('BUY')
    else:
        self.orders.append("SELL")

    #More example logic
    return self.orders
    