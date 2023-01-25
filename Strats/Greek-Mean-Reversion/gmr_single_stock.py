import time
import collections
import math
import statistics

#Greek Mean Reversion Template, Single Stock.
class gmr_strat():
    """
    A strategy using a simple moving average, as well as two bands of two standard deviations +- the moving average.
    """
    def __init__(self, metrics, initvalues):
        """
        Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
        Initvalues - the initial values of your arguments. 
        """
        self.data = zip(metrics,initvalues)
        self.time = time.time()
        self.orders = []
        self.ticks = 0
