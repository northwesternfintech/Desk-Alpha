import collections
import math
import time

class bollinger_multi():

    def __init__(self, tickers, days, stdDevs, MAcalc):
        """
        Constructor for Bollinger Bands. If price goes above the upper band, add a sell order, if price goes below the lower band, add a buy order.
        """

        self.data = {}
        self.orders = {}
        #data for the day, ticker : [open, high, low, close]
        self.dayData = {}
        self.time = time.time()
        self.ticks = 0
        #data used to calculate moving average, ticker : list[days]. list contains [open, high, low, close]
        self.MAdict = {}
        #bollinger bands, ticker : [upper, lower]
        self.bbs = {}
        for ticker in tickers:
            self.data[ticker] = []
            self.orders[ticker] = []
            self.dayData[ticker] = [-1, -1, math.inf, -1]
            self.MAdict[ticker] = []
            self.bbs[ticker] = [0,0]

        #how many standard deviations to use
        self.stdevs = stdDevs

        #how many days to use for moving average
        self.days = days

        def clear_orders(self, ticker):
            """
            Clears the orders to be executed.
            """
            self.orders[ticker] = []
        
        def calcStdDev(self, ticker):
            """
            Calculates the standard deviation of the data
            """
            mean = sum(self.MAdict[ticker])/self.days
            total = 0.0
            for price in self.MAdict[ticker]:
                total += (price - mean)**2
            return math.sqrt(total/self.days)
        
        def update(self,ticker,price):
            """
            Updates the strategy with new information.
            """
            #update the day data
            if self.dayData[ticker][0] == -1:
                self.dayData[ticker][0] = price
            self.dayData[ticker][1] = max(self.dayData[ticker][1], price)
            self.dayData[ticker][2] = min(self.dayData[ticker][2], price)
            self.dayData[ticker][3] = price

            if len(self.MAdict[ticker]) > self.days:
                self.MAdict[ticker].pop(0)
            if len(self.MAdict[ticker]) == self.days:
                stdev = self.calcStdDev(ticker)
                mean = sum(self.MAdict[ticker])/self.days

                lowerBand = mean - self.stdevs*stdev
                upperBand = mean + self.stdevs*stdev

                self.bbs[ticker][0] = upperBand
                self.bbs[ticker][1] = lowerBand

                if price > upperBand:
                    self.orders[ticker].append('SELL')
                elif price < lowerBand:
                    self.orders[ticker].append('BUY')
        

        def updateAll(self, newData):
            """
            calls update on all tickers
            """
            for ticker,price in newData.items():
                self.update(ticker, price)
            self.ticks += 1


