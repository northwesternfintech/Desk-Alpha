import time
import collections
import math

#Simple multiple stock template
#Notes: I turned self.orders into a dictionary where the key is the stock ticker and the value is buy, sell, or stay (do nothing)
#Trend has also become a metric for each stock rather than for the entire class

class multipleStockTemplateStrategy():
  """
  A base strategy that is used to explain how to properly develop a strategy for multiple stocks
  """
  
  def __init__(self, allInitStockData):
    """
    allStockInitData - a dictionary where the keys are stock tickers and...
    the values are dictionaries with metrics as keys and initvalues as values
    Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    Initvalues - the initial values of your arguments. 
    """
    self.data = allInitStockData
    for stock in allInitStockData:
      self.data[stock]['trend'] = "Downward" #should be this way so we buy whenever price goes up for first time

    self.time = time.time()
    self.orders = dict()
    self.ticks = 0
    
  #YOU WILL WANT A FULL SUITE OF SETTER AND GETTER METHODS!
  def get_data(self):
    return self.data
  def get_time(self):
    return self.time
  def get_orders(self):
    return self.orders
  def get_ticks(self):
    return self.ticks
  def get_stock_data(self, ticker):
    return self.data[ticker]

  def set_data(self, newData):
    self.data = newData
  def set_time(self, newTime):
    self.time = newTime
  def set_orders(self, newOrders):
    self.orders = newOrders
  def set_ticks(self, newTicks):
    self.ticks = newTicks

  def set_stock_data(self, ticker, newData):
    for metric in newData:
      self.data[ticker][metric] = newData[metric] #update data
  
  def update_stock(self, ticker, newData):
    """
    Updates information for one stock given new data and adds the necessary order for that stock to the orders dict
    newData should be a dict with metrics and values only that corresponds to data for the stock with the ticker
    @type ticker: str
    @type newData: dict
    """
    previousPrice = self.data[ticker]['price'] #set previous price and update stock data
    self.set_stock_data(ticker, newData) 

    newPrice = newData['price'] #set new price and current trend
    currentTrend = self.data[ticker]['trend']

    priceUpdated = False #variable to track if price has been updated

    if newPrice>previousPrice: #if price of this stock goes up...
      if currentTrend == "Downward":  #if this stock was previously going down...
        self.orders[ticker] = "BUY" #set order for stock to BUY
        priceUpdated = True
      self.data[ticker]['trend'] = "Upward" #set new trend to upward
    
    elif newPrice<previousPrice: #if price of this stock goes down...
      if self.get_trend() == "Upward": #if this stock was previously going up
        self.orders[ticker] = "SELL" #set order for stock to SELL
        priceUpdated = True
      self.data[ticker]['trend'] == "Downward" #set new trend to downward

    if not priceUpdated: 
      self.orders[ticker] = "STAY" #if we are not buying or selling, set order for stock to STAY

  
def clear_orders(self):
    """
    Clears all current orders and logs relevant information.
    """
    print(f"Trashing %d orders.", len(self.orders))
    self.orders = dict()
    
def update(self, newAllStockData):
  """
  Will be called on every tick to update the algorithm state and output buys/sells/stays for all stocks
  newAllStockData should be a dict with tickers as keys and values being dictionaries that have keys being our metrics
  @type newAllStockData: dict 
  @rtype: dict
  """
  self.clear_orders()
  self.ticks += 1

  for thisStock in newAllStockData:             #run update_stock for each stock in newAllStockData
    newStockData = newAllStockData[thisStock]   #newStockData will be a dictionary 
    self.update_stock(thisStock, newStockData)

  return self.orders 
  #orders for the stocks are returned in the the dictionary with the key being stock ticker and value being buy/sell/stay
    