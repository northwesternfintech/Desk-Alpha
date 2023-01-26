# -*- coding: utf-8 -*-
import FibonacciSingleStock
#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.
class FibonacciMultiStock(FibonacciSingleStock):
  
    def __init__(self, scope = 900, ordersWhenHitsBand = 1, num):

        #stores number of stocks we are analyzing
        self.num = num
        #used to store the lerp bands, being a matrix of size 7 * num
        self.bands = [0, 0, 0, 0, 0, 0, 0] * num
  

    def calculateRetracementMulti(self):
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

