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
    self.state = "Up"
#YOU WILL WANT A FULL SUITE OF SETTER AND GETTER METHODS!

def get_data(self, metric):
    """
    Returns the current data.
    """
    return self.data[metric]

def set_data(self, metric, value):
    """
    Sets the current data.
    """
    self.data[metric] = value


def get_time(self):
    """
    Returns the time since the last tick.
    """
    return self.time

def set_time(self, time):
    """
    Sets the time since the last tick.
    """
    self.time = time

def get_orders(self):
    """
    Returns the current orders.
    """
    return self.orders

def set_orders(self, orders):
    """
    Sets the current orders.
    """
    self.orders = orders

def get_ticks(self):
    """
    Returns the number of ticks since the last reset.
    """
    return self.ticks

def set_ticks(self, ticks):
    """
    Sets the number of ticks since the last reset.
    """
    self.ticks = ticks


def clear_orders(self):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d orders.", len(self.orders))
    self.orders = []

def get_state(self):
    """
    Returns the current state of the algorithm.
    """
    return self.state

def set_state(self, state):
    """
    Sets the current state of the algorithm.
    """
    self.state = state

def update(self, data):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    """
    self.ticks += 1
    #Ingest Data

    old_price = self.data['price']
    updates = zip(data.keys(), data.values())
    for metric, information in updates:
      self.data[metric] = information


    self.clear_orders()
    #Re-run your logic


    if self.data['price'] < old_price : #If the new price is going down compared to old
        if self.get_state() == "Up": #If state indicates we were previously going up
             self.orders.append('SELL') #Sell
        self.set_state("Down") # Reverse the state

    elif self.data['price'] > old_price : #If the price is going down
        if self.get_state() == "Up": #If state indicates we were going up
            self.orders.append('BUY') #Buy
        self.set_state("Down")  # Reverse the state by setting it to down

    #More example logic
    return self.orders


