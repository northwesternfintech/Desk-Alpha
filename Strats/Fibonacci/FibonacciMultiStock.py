# -*- coding: utf-8 -*-
import collections
import math

#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.
class FibonacciMultiStock():
    def __init__(self, scope = 900, ordersWhenHitsBand = 1, **kwargs):
        #How many ticks back we should look when creating retracement
        self.scope = scope
        #how many orders we'd like to put in when the price bounces off a band
        self.ordersWhenHitsBand = ordersWhenHitsBand
        # general data dict, not used here, but keeping in case needed for revisions later
        self.data = {}
        # stores ticker: orders
        self.orders = {}
        # Stands for typical price. stores ticker: list of len(MAL) where self.TP[ticker][i] contains that days [open, high, low, close]
        self.typicalPrices = {}
        # contains ticker: [open, high, low, close] of current day. Reset at beginning of each day
        self.dayData = {}
        # stores ticker: lower band, upper band
        self.bands = {}

        tickers = kwargs["tickers"]
        for ticker in tickers:
            self.data[ticker] = []
            self.orders[ticker] = []
            self.typicalPrices[ticker] = []
            self.dayData[ticker] = [-1, -1, math.inf, -1]
            self.bands[ticker] = [0, 0, 0, 0, 0, 0, 0]
        
        #stores constant ratios—can change to be mutable later if needed
        self.ratios = [0,0.236, 0.382, 0.5 , 0.618, 0.786,1]

        #used to store when we need to create a new retracement
        self.nextRetracement = scope
        self.ticks = 0

        #used to make sure we dont retrace before we have enough data to do so
        self.activeRetracement = False

    def clear_orders(self, ticker):
        """
        Clears all current orders and logs relevant information.
        """
        print(f"Trashing %d orders.", len(self.orders[ticker]))
        self.orders[ticker] = []

    def calculateRetracementSingle(self, ticker):
        """calculate fibonacci retracement bands"""
        #calculating for the nth stock
        #print("data is", self.data[ticker])
        #print("calculating")
        low = (10**9, 0)
        high = (-10**9, 0)
        for i in range(self.scope):
            #print(self.data[ticker][(i+1)*-1], i)
            if self.data[ticker][(i+1)*-1] > high[0]:
                #print("found a new high at i", i)
                high = (self.data[ticker][(i+1)*-1], i)
            if self.data[ticker][(i+1)*-1] < low[0]:
                #print("found a new low at i", i)
                low = (self.data[ticker][(i+1)*-1], i)
        #print("low is ", low[0], "at i ", low[1])
        #print("high is", high[0], "at i ", high[1])
        #incline
        if low[1] > high[1]:
            #print("here hehe xd")
            l, r = low[0], high[0]
            self.bands[ticker][0] = r
            self.bands[ticker][-1] = l
            for i in range(len(self.ratios)):
                self.bands[ticker][len(self.bands)-1-i] = l + (r-l) * self.ratios[i]

        #decline
        elif low[1] < high[1]:
            #print("here at", self.ticks)
            l, r = high[0], low[0]
            self.bands[ticker][0] = r
            self.bands[ticker][-1] = l
            for i in range(len(self.ratios)):
                self.bands[ticker][len(self.bands)-1-i] = l + (r-l) * self.ratios[i]

    def updateSingle(self, **kwargs):
        """
        Update method called every tick. Just takes in the stock's price at the time of the tick
        """
        #updating for the nth stock
        #if the tick we're at is equal to our defined time for when the next "retracement" period starts, make note
        #of it and create our new bands
        ticker = kwargs["ticker"]
        price = kwargs["price"]

        if self.activeRetracement:
            prev = self.data[ticker][-1]
            #print(prev, price)
            #incline
            if self.bands[ticker][0] > self.bands[ticker][-1]:
                #check if our current price compared w our prev price has crossed any of the bounds
                for band in self.bands[ticker]:
                    if prev >= band and price <=band:
                        for i in range(self.ordersWhenHitsBand):
                            #if before we were inclined, then we started going down and bounced off a band,
                            #add a buy order
                            self.orders[ticker].append("BUY")
            #decline
            elif self.bands[ticker][0] < self.bands[ticker][-1]:
                for band in self.bands[ticker]:
                    if prev <= band and price >= band:
                        for i in range(self.ordersWhenHitsBand):
                            #if before we declined, then started going up and bounced off a band, add a sell order                      
                            self.orders[ticker].append("SELL")
        self.data[ticker].append(price)
        return self.orders
        

    def updateAll(self, newData):
        if self.ticks == self.nextRetracement:
                self.nextRetracement = self.ticks + self.scope
                if not self.activeRetracement: self.activeRetracement = True
                for ticker, price in newData.items():
                    self.calculateRetracementSingle(ticker)
        for ticker, price in newData.items():
            self.updateSingle(ticker=ticker, price=price)
        self.ticks += 1
        print(self.ticks)

"""
f = FibonacciMultiStock(10, 1, **{"tickers": ["A", "B", "C"], "dayConst": 60, "MAL": 20, "bandSD": 2, "clearDataLen": 10000})
f.updateAll({"A": 3.0, "B": 5.0, "C": 8.0})
f.updateAll({"A": 4.0, "B": 6.0, "C": 9.0})
f.updateAll({"A": 5.0, "B": 7.0, "C": 8.0})
f.updateAll({"A": 6.0, "B": 8.0, "C": 8.0})
f.updateAll({"A": 7.0, "B": 9.0, "C": 8.0})
f.updateAll({"A": 8.0, "B": 10.0, "C": 8.0})
f.updateAll({"A": 9.0, "B": 11.0, "C": 8.0})
f.updateAll({"A": 8.0, "B": 10.0, "C": 8.0})
f.updateAll({"A": 7.0, "B": 9.0, "C": 8.0})
f.updateAll({"A": 6.0, "B": 8.0, "C": 8.0})
f.updateAll({"A": 5.0, "B": 7.0, "C": 8.0})
f.updateAll({"A": 4.0, "B": 6.0, "C": 8.0})
f.updateAll({"A": 3.0, "B": 5.0, "C": 8.0})
f.updateAll({"A": 100.0, "B": 100.0, "C": 100.0})
print(f.bands)
print(f.orders)
"""