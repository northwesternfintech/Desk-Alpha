from signal import Sigmasks
import collections
import math
#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.
class BollingerBandsSingleStock:
  
    def __init__(self, dayConst = 60, MAL = 20, bandSD = 2, clearDataLen = 10000):
        """
        Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
        Initvalues - the initial values of your arguments. 
        """
        #general data dict, not used here, but keeping in case needed for revisions later
        self.data = []
        #stores ticker: orders
        self.orders = []
        #Stands for typical price. stores ticker: list of len(MAL) where self.TP[ticker][i] contains that days [open, high, low, close]
        self.TP = []
        #contains ticker: [open, high, low, close] of current day. Reset at beginning of each day
        self.dayData = [-1, -1, math.inf, -1]
        #stores ticker: lower band, upper band
        self.bands = [0, 0]


        self.ticks = 0
        #stores how many ticks we want there to be in each day. By default set to 60, or every hour
        self.dayConst = dayConst
        #stores how many previous days' data we want to use in our moving average. By default set to 20
        self.MAL = MAL
        #stores how many standard deviations we want to use to calculate our upper and lower bands. By default set to 2
        self.bandSD = bandSD
        #stores when our next day stats (in ticks)
        self.nextDayStart = dayConst
        #variable to clear our least recent orders so that the length of the list doesnt get too big. By default set to 10,000
        self.clearDataLen = clearDataLen
  
    

    def clear_orders(self):
        """
        Clears all current orders and logs relevant information.
        """
        print(f"Trashing %d orders.", len(self.orders))
        self.orders = []

    def getSigma(self):
        #general purpuse method which calculates the standard deviation for a tickers TP in last MAL days
        mean = sum(self.TP)/self.MAL
        total = 0.0
        for price in self.TP:
            total+=(price-mean)**2
        total/=self.MAL
        return total**0.5

    #update method
    def update(self, price):
        self.ticks+=1
        newDay = False
        if self.ticks == self.nextDayStart:
            self.nextDayStart = self.ticks + self.dayConst 
            newDay = True
        
        if newDay:
            #handle all new day management stuff
            #if we're at a new day, add our current day's data to TP and reset the dayData 
            self.TP.append(sum(self.dayData)/4)
            self.dayData = [-1, price, price, price]

        #open, high, low, close — update all accordingly
        #update open only once
        if self.dayData[0] == -1:
            self.dayData[0] = price
        self.dayData[1] = max(self.dayData[1], price)
        self.dayData[2] = min(self.dayData[1], price)
        self.dayData[3] = price


        #only run core logic if algo has been running for at least MAL ticks
        if len(self.TP) > self.MAL:
            self.TP.pop(0)
            #get appropriate stats
        if len(self.TP) == self.MAL:
            sig = self.getSigma()
            mean = sum(self.TP)/self.MAL

            lowerBand = mean-self.bandSD*sig
            upperBand = mean+self.bandSD*sig
            #update appropriate bands
            self.bands[0] = lowerBand
            self.bands[1] = upperBand
            #print("TICK:", self.ticks)
            #print("MEAN:", mean)
            #print("PRICE:", price)
            #print("BANDS:", self.bands)
            #print("ORDERS:", self.orders)
            

            if price > upperBand:
                #print("ADDING SELL ORDER")
                self.orders.append("SELL")
            elif price < lowerBand:
                #print("ADDING BUY ORDER")
                self.orders.append("BUY")
            #print()

            if len(self.orders) > self.clearDataLen:
                self.orders.pop(0)
"""BB = BollingerBandsSingleStock(4, 4, 2, 100)

BB.update(59)
BB.update(62)
BB.update(59)
BB.update(54)
BB.update(57)

BB.update(65)
BB.update(68)
BB.update(75)
BB.update(69)
BB.update(63)

BB.update(58)
BB.update(42)
BB.update(39)
BB.update(48)
BB.update(57)

BB.update(59)
BB.update(68)
BB.update(73)
BB.update(73)
BB.update(58)

#print(BB.TP)
#print(BB.bands)"""
