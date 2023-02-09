import time
import collections
import math

#Single-stock for option volatility gamma delta trading strategy

class vol_gamma_delta():
  """
  Single-stock for option volatility gamma delta trading strategy
  """
  
  def __init__(self, initData):
    """
    initData: dictionary with key "gamma" and value gamma
    """
    self.data = initData
    self.time = time.time()
    self.orders = []
    self.hasPut = False
    self.hasCall = False
    self.ticks = 0
  
def clear_orders(self):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d orders.", len(self.orders))
    self.orders = []
    
def update(self, data):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    data should be a dictionary that contains "gamma" as key and value of gamma as value
    """
    #update gamma and ticks and clear orders
    self.ticks += 1
    updates = zip(data.keys(), data.values())
    for metric, information in updates:
      self.data[metric] = information 
    self.clear_orders()

    #run logic
    if self.data['gamma'] >= 50 and not self.hasCall:
      self.orders.append('BUY CALL')
      self.orders.append('BUY PUT')
      self.hasCall = True
      self.hasPut = True

    if self.data['gamma'] >= 55 and self.hasCall:
      self.orders.append('EXERCISE CALL')
      self.hasCall = False
    elif self.data['gamma'] <= 40:
      self.orders.append('SELL PUT')
      self.hasPut = False

    return self.orders