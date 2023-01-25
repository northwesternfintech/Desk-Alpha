import time
import math
import pyblackscholesanalytics as bs

#Greek Mean Reversion Template, Single Stock.
#Documentation: https://docs.google.com/document/d/1lV_E_UPckYBPbx_C3F3EbQbss8uFPQ_fr0pxpGBe3dU/edit?usp=sharing
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
    
    def __init__(self, **kwargs):
        self.data = kwargs
        self.time = time.time()
        self.orders = []
        self.ticks = 0
