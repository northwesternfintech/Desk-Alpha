import time
import collections
import math
import statistics

#Bollinger Band Template, Single Stock.


class bollingerStrategy():
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
    
    def get_data(self, metric):
        """
        Returns the data for a given metric.
        """
        return self.data[metric]

    def set_data(self, metric, value):
        """
        Sets the value of a metric.
        """
        self.data[metric] = value

    def get_time(self):
        """
        Returns the time since the last update.
        """
        return self.time

    def set_time(self, time):
        """
        Sets the time since the last update.
        """
        self.time = time

    def get_ticks(self):
        """
        Returns the number of ticks that have passed.
        """
        return self.ticks

    def set_ticks(self, ticks):
        """
        Sets the number of ticks that have passed.
        """
        self.ticks = ticks

    def get_orders(self):
        """
        Returns the current orders.
        """
        return self.orders

    def set_orders(self, orders):
        """
        Sets the orders to be executed.
        """
        self.orders = orders

    def clear_orders(self):
        """
        Clears the orders to be executed.
        """
        self.orders = []

    def update(self, data):
        """
        Updates the strategy with new information.
        """
        self.ticks += 1
        updates = zip(data.keys(), data.values())
        for metric, information in updates:
            self.data[metric] = information
        

        self.clear_orders()
        moving_average = 0
        for price in self.data['prices'][-20:]:
            moving_average += price
        moving_average /= 20
        standard_deviation = 0
        for price in self.data['prices'][-20:]:
            standard_deviation += (price - moving_average)**2
        standard_deviation = math.sqrt(standard_deviation/20)

        upper_band = moving_average + 2*standard_deviation
        lower_band = moving_average - 2*standard_deviation
        if self.data['price'] > upper_band:
            self.orders.append('SELL')
        elif self.data['price'] < lower_band:
            self.orders.append('BUY')
        #else:
        #    self.orders.append('HOLD')
        #return self.orders