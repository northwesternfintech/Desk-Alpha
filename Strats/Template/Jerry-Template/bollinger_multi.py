import collections
import math

class bollinger_multi():

    def __init__(self, tickers, days, stdDevs):
        """
        Constructor for Bollinger Bands. If price goes above the upper band, add a sell order, if price goes below the lower band, add a buy order.
        """

        self.data = {}
        