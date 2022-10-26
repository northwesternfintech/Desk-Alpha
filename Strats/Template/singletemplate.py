import time
import collections
import math

#Very simple single-stock template. We will be generating these to get started with a simple strategy, and then generalizing it outward.

class templateStrategy():
```
A base strategy that is used to explain how to properly develop a strategy.
```
  
  def __init__(self, metrics, initvalues):
    ```
    #Metrics - the actual information you need to track. If this is a specific algorithm, you can hard-code it and remove that argument.
    #Initvalues - the initial values of your arguments. 
    ```
    self.data = zip(metrics,initvalues)
    self.time = time.time()
    self.orders = []
    self.ticks = 0
#YOU WILL WANT A FULL SUITE OF SETTER AND GETTER METHODS!
  
  def clear_orders(self):
    ```
    Clears all current orders and logs relevant information.
    ```
    print(f"Trashing %d orders.", len(self.orders))
    self.orders = []
    
  def update(self, data):
    ```
    Will be called on every tick to update the algorithm state and output buys/sells.
    ```
    #Ingest Data
    updates = zip(data.keys(), data.values())
    for metric, information in updates:
      self.data[metric] = information
      
    self.clear_orders()
    #Re-run your logic
    if self.data['price'] > 100:
      self.orders.append('BUY')
    #More example logic
    return self.orders
    
