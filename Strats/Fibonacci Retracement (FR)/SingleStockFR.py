import time
import collections
import math

# Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.


class FibonacciRetracementSingleStock:
    """
    A base strategy that is used to explain how to properly develop a strategy.
    """

    def __init__(self, metrics, initvalues):
        """
        Metrics - the actual information you need to track.
        Initvalues - the initial values of your arguments.
        """
        self.data = zip(metrics, initvalues)
        self.time = time.time()
        self.orders = []
        self.ticks = 0
        self.prev = 0

    def clear_orders(self):
        """
        Clears all current orders and logs relevant information.
        """
        print(f"Trashing %d orders.", len(self.orders))
        self.orders = []

    def calculate_retracement(self, high, low):
        """
        This function calculates the Fibonacci retracement levels based on the high and low values.
        """
        # Calculate the vertical distance between the high and low values
        vertical_distance = high - low

        # Calculate the retracement levels using Fibonacci ratios
        retracement_levels = {}
        retracement_levels["23.6%"] = low + (vertical_distance * 0.236)
        retracement_levels["38.2%"] = low + (vertical_distance * 0.382)
        retracement_levels["50%"] = low + (vertical_distance * 0.5)
        retracement_levels["61.8%"] = low + (vertical_distance * 0.618)

        return retracement_levels

    def update(self, data):
        """
        Will be called on every tick to update the algorithm state and output buys/sells.
        """
        self.ticks += 1
        # Ingest Data
        updates = zip(data.keys(), data.values())
        for metric, information in updates:
            self.data[metric] = information

        self.clear_orders()

        # Calculate retracement levels using the high and low values
        high = self.data["high"]
        low = self.data["low"]
        retracement_levels = self.calculate_retracement(high, low)

        if self.data["price"] > retracement_levels["61.8%"]:
            self.orders.append("SELL")
        elif self.data["price"] < retracement_levels["23.6%"]:
            self.orders.append("BUY")
        return self.orders
