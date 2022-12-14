import math

# Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.
class BollingerBandsSingleStock:
    def __init__(self, dayConst=60, MAL=20, bandSD=2, clearDataLen=10000):
        """
        Constructor for single stock Bollinger Bands algo. If the stock price exceeds the upper band, add a sell order,
        and if it goes below the lower band, add a buy order.
        """
        # general data dict, not used here, but keeping in case needed for revisions later
        self.data = []
        # stores ticker: orders
        self.orders = []
        # Stands for typical price. stores ticker: list of len(MAL) where self.TP[ticker][i] contains that days [open, high, low, close]
        self.typicalPrices = []
        # contains ticker: [open, high, low, close] of current day. Reset at beginning of each day
        self.dayData = [-1, -1, math.inf, -1]
        # stores ticker: lower band, upper band
        self.bands = [0, 0]

        self.ticks = 0
        # stores how many ticks we want there to be in each day. By default set to 60, or every hour
        self.ticksPerDay = dayConst
        # stores how many previous days' data we want to use in our moving average. By default set to 20
        self.daysInMovingAverage = MAL
        # stores how many standard deviations we want to use to calculate our upper and lower bands. By default set to 2
        self.bandSigmaFromMean = bandSD
        # stores when our next day stats (in ticks)
        self.nextDayStart = dayConst
        # variable to clear our least recent orders so that the length of the list doesnt get too big. By default set to 10,000
        self.clearDataLen = clearDataLen

    def clear_orders(self):
        """
        Clears all current orders and logs relevant information.
        """
        print(f"Trashing %d orders.", len(self.orders))
        self.orders = []

    def getSigma(self):
        """
        Returns the standard deviation data in self.typicalPrices. Follows standard sigma formula
        """
        mean = sum(self.typicalPrices) / self.daysInMovingAverage
        total = 0.0
        for price in self.typicalPrices:
            total += (price - mean) ** 2
        total /= self.daysInMovingAverage
        return total**0.5

    def update(self, price):
        """
        Update method called every tick. Just takes in the stock's price at the time of the tick
        """

        newDay = False
        # if the tick we're at is equal to our defined time for when the next "day" starts, make note of the fact that we're
        # on a new "day" and update the time of the next "day" start.
        if self.ticks == self.nextDayStart:
            self.nextDayStart = self.ticks + self.ticksPerDay
            newDay = True

        if newDay:
            # handle all new day management stuff
            # if we're at a new day, add our current day's data to TP and reset the dayData
            self.typicalPrices.append(sum(self.dayData) / 4)
            self.dayData = [-1, price, price, price]

        # open, high, low, close — update all accordingly
        # update open only once
        if self.dayData[0] == -1:
            self.dayData[0] = price
        self.dayData[1] = max(self.dayData[1], price)
        self.dayData[2] = min(self.dayData[2], price)
        self.dayData[3] = price

        # only run core logic if algo has been running for at least MAL ticks
        if len(self.typicalPrices) > self.daysInMovingAverage:
            self.typicalPrices.pop(0)
            # get appropriate stats
        if len(self.typicalPrices) == self.daysInMovingAverage:
            sig = self.getSigma()
            mean = sum(self.typicalPrices) / self.daysInMovingAverage

            lowerBand = mean - self.bandSigmaFromMean * sig
            upperBand = mean + self.bandSigmaFromMean * sig
            # update appropriate bands
            self.bands[0] = lowerBand
            self.bands[1] = upperBand

            if price > upperBand:
                # print("ADDING SELL ORDER")
                self.orders.append("SELL")
            elif price < lowerBand:
                # print("ADDING BUY ORDER")
                self.orders.append("BUY")
            # print()

            if len(self.orders) > self.clearDataLen:
                self.orders.pop(0)
        self.ticks += 1
