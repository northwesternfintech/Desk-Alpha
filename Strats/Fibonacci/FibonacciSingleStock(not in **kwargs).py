# -*- coding: utf-8 -*-
import collections
import math
#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.
class FibonacciSingleStock:
  
    def __init__(self, scope = 900, ordersWhenHitsBand = 1):
        """
        Constructor for single stock Bollinger Bands algo. If the stock price exceeds the upper band, add a sell order, 
        and if it goes below the lower band, add a buy order.
        """
        #general data used to store previous prices
        self.data = []
        #How many ticks back we should look when creating retracement
        self.scope = scope
        #how many orders we'd like to put in when the price bounces off a band
        self.ordersWhenHitsBand = ordersWhenHitsBand
        #stores orders
        self.orders = []
        #stores constant ratios—can change to be mutable later if needed
        self.ratios = [0,0.236, 0.382, 0.5 , 0.618, 0.786,1]
        #used to store the lerp bands
        self.bands = [0, 0, 0, 0, 0, 0, 0]

        #used to store when we need to create a new retracement
        self.nextRetracement = scope
        self.ticks = 0

        #used to make sure we dont retrace before we have enough data to do so
        self.activeRetracement = False
  

    def clear_orders(self):
        """
        Clears all current orders and logs relevant information.
        """
        self.orders = []

    def calculateRetracement(self):
        """calculate fibonacci retracement bands"""
        #print("data is", self.data)
        #print("calculating")
        low = (10**9, 0)
        high = (-10**9, 0)
        for i in range(self.scope):
            #print(self.data[(i+1)*-1], i)
            if self.data[(i+1)*-1] > high[0]:
                #print("found a new high at i", i)
                high = (self.data[(i+1)*-1], i)
            if self.data[(i+1)*-1] < low[0]:
                #print("found a new low at i", i)
                low = (self.data[(i+1)*-1], i)
        #print("low is ", low[0], "at i ", low[1])
        #print("high is", high[0], "at i ", high[1])
        #incline
        if low[1] > high[1]:
            #print("here hehe xd")
            l, r = low[0], high[0]
            self.bands[0] = r
            self.bands[-1] = l
            for i in range(len(self.ratios)):
                self.bands[len(self.bands)-1-i] = l + (r-l) * self.ratios[i]

        #decline
        elif low[1] < high[1]:
            #print("here at", self.ticks)
            l, r = high[0], low[0]
            self.bands[0] = r
            self.bands[-1] = l
            for i in range(len(self.ratios)):
                self.bands[len(self.bands)-1-i] = l + (r-l) * self.ratios[i]

    def update(self, price):
        """
        Update method called every tick. Just takes in the stock's price at the time of the tick
        """
        
        #if the tick we're at is equal to our defined time for when the next "retracement" period starts, make note
        #of it and create our new bands
        if self.ticks == self.nextRetracement:
            self.nextRetracement = self.ticks + self.scope
            if not self.activeRetracement: self.activeRetracement = True
            self.calculateRetracement()

        if self.activeRetracement:
            prev = self.data[-1]
            #print(prev, price)
            #incline
            if self.bands[0] > self.bands[-1]:
                #check if our current price compared w our prev price has crossed any of the bounds
                for band in self.bands:
                    if prev >= band and price <=band:
                        for i in range(self.ordersWhenHitsBand):
                            #if before we were inclined, then we started going down and bounced off a band,
                            #add a buy order
                            self.orders.append("BUY")
            #decline
            elif self.bands[0] < self.bands[-1]:
                for band in self.bands:
                    if prev <= band and price >=band:
                        for i in range(self.ordersWhenHitsBand):
                            #if before we declined, then started going up and bounced off a band, add a sell order                      
                            self.orders.append("SELL")
        self.ticks+=1
        self.data.append(price)
        return self.orders

"""f = FibonacciSingleStock(10, 1)
f.update(10)
f.update(11)
f.update(12)
f.update(13)
f.update(14)
f.update(15)
f.update(16)
f.update(15)
f.update(14)
f.update(15)
f.update(13)


print(f.bands)
print(f.orders)

f.update(13)
f.update(12)
f.update(11)
f.update(10)
f.update(9)
f.update(8)
f.update(7)
f.update(6)
f.update(8)
f.update(7)
f.update(6)

f.update(9)
f.update(10)


print(f.bands)
print(f.orders)"""

