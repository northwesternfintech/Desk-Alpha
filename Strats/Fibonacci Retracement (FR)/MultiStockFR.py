import time
import collections
import math

class FibonacciRetracementStrategy():
  """
  A strategy that uses Fibonacci retracement levels to determine support and resistance levels for multiple stocks.
  """

  def __init__(self,metrics, **kwargs):
    """
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments.
    initvalues should be a dictionary with stock symbols as keys and a list of values that correspond to the metrics in the same order as they appear in the metrics variable.
    Example:
    metrics = ['price', 'high', 'low']
    initvalues = {'AAPL': [100, 110, 90], 'GOOG': [200, 220, 180]}
    """
    self.data = {}
    self.time = time.time()
    self.orders = {}
    self.ticks = 0
    self.prev = {}
    self.metrics = metrics
    initvalues = kwargs.get('initvalues', {})
    for stock in initvalues.keys():
      self.data[stock] = {}
      self.prev[stock] = {}
      self.orders[stock] = []
      for metric, value in zip(metrics, initvalues[stock]):
        self.data[stock][metric] = value
        self.prev[stock][metric] = value

  def clear_orders(self):
    """
    Clears all current orders and logs relevant information.
    """
    for stock in self.orders.keys():
      print(f"Trashing %d orders for stock %s", len(self.orders[stock]), stock)
      self.orders[stock] = []

  def calculate_retracement(self, data):
    """
    Calculates Fibonacci retracement levels for a given stock.
    """
    retracement_levels = {}
    for stock in data.keys():
      high = data[stock]['high']
      low = data[stock]['low']
      retracement_levels[stock] = {}
      retracement_levels[stock]['23.6%'] = low + (high - low) * 0.236
      retracement_levels[stock]['38.2%'] = low + (high - low) * 0.382
      retracement_levels[stock]['50%'] = low + (high - low) * 0.5
      retracement_levels[stock]['61.8%'] = low + (high - low) * 0.618
    return retracement_levels

  def update(self, data):
    """
    Will be called on every tick to update the algorithm state and output buys/sells.
    """
    self.ticks += 1
    #Ingest Data
    updates = zip(data.keys(), data.values())
    for stock, stock_data in updates:
      for metric, information in zip(self.metrics, stock_data):
        self.data[stock][metric] = information

    self.clear_orders()
    #Calculate retracement levels for each stock
    retracement_levels = self.calculate_retracement(self.data)
    #Re-run your logic
    for stock in self.data.keys():
      if self.data[stock]['price'] > retracement_levels[stock]['50%']:
        self.orders[stock].append('SELL')
      elif self.data[stock]['price'] < retracement_levels[stock]['50%']:
        self.orders[stock].append('BUY')
    return self.orders