import time
import collections
import math

#Very simple multiple-stock template.
# Turn self.order into dictionary where key is stock ticker and value is buy/sell or nothing (empty string)
# Trend has become a metric for each stock rather than a single metric for the class

class multipleStocksTemplateStrategy():
  """
  A base strategy that is used to explain how to properly develop a strategy for multiple stocks
  """

  def __init__(self, metrics, allStockInItValues):
    """
    allStockInitValues - a dictionary where the key is the stock tickers and the value is a list of initial values for the metrics
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments.
    """
    self.data = allStockInItValues

    for stock in self.data:
      self.data[stock]['trend'] = "Down"   # Initialize trend to down for each stock

    self.time = time.time()
    self.orders = {}
    self.ticks = 0

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

def get_stock_data(self, ticker):
    """
    Returns the current state of the specified stock.
    """
    return self.data[ticker]

def set_stock_data(self, ticker, data):
    """
    Sets the current state of the specified stock.
    """
    for metric in data:
        self.data[ticker][metric] = data[metric]

def update_stock(self, ticker, newData):
    """
    Updates information for one stock given new data and adds the necessary order for that stock to the orders dict
    ticker - the stock ticker (string)
    newData - a dictionary of the current data for the stock (dictionary)
    """
    # Update the data for the stock
    previous_price = self.data[ticker]['price'] #set previous price and update stock data
    self.set_stock_data(ticker, newData)

    new_price = newData['price'] #set new price and current trend
    current_trend = self.data[ticker]['trend']

    price_updated = False #variable to track if price has been updated

    if new_price>previous_price: #if price of this stock goes up...
      if current_trend == "Down":  #if this stock was previously going down...
        self.orders[ticker] = "BUY" #set order for stock to BUY
        price_updated = True
      self.data[ticker]['trend'] = "Up" #set new trend to upward

    elif new_price<previous_price: #if price of this stock goes down...
      if self.get_trend() == "Up": #if this stock was previously going up
        self.orders[ticker] = "SELL" #set order for stock to SELL
        price_updated = True
      self.data[ticker]['trend'] = "Down" #set new trend to downward

    if not price_updated:
      self.orders[ticker] = "" #if we are not buying or selling, set order for stock to empty string


def update(self, newStockDataAll):
  """
  Will be called on every tick to update the algorithm state and output buys/sells/stays for all stocks
  newAllStockData should be a dict with tickers as keys and values being dictionaries that have keys being our metrics
  @type newAllStockData: dict
  @rtype: dict
  """
  self.clear_orders() #clear all orders from previous tick
  self.ticks += 1

  for stock in newStockDataAll:             #run update_stock for each stock in newAllStockData
    new_stock_data = newStockDataAll[stock]   #newStockData will be a dictionary
    self.update_stock(stock, new_stock_data)

  return self.orders
  #orders for the stocks are returned in the the dictionary with the key being stock ticker and value being buy/sell/stay
