import math
import matplotlib.pyplot as plt
import numpy as np
import time

class Var_sampler:
    # alpha is how much you want variability to matter, measured 0-1.
    # beta is where you want the cutoff for variable sampling to be, measured as a percent tolerance in price standard deviation.
    # base rate is how many times per second you want the sample to be taken.
    def __init__(self, base_rate, alpha, beta, sample, lookback):
        self.base_rate = base_rate
        self.alpha = alpha
        self.beta = beta
        self.sample = sample
        self.previous_sample_time = 0
        self.lookback = lookback
        self.sampled = np.array([])

    def run(self):
        while True:
            history = self.sampled[-self.lookback:]
            if time.time() - self.previous_sample_time >= 1/self.base_rate:
                self.add_sample()
            elif (len(self.sampled) > self.lookback) and (np.std(history)/np.mean(history) > self.beta):
                self.add_sample()
            else:
                pass
                
    def add_sample(self):
        self.sampled = np.append(self.sampled, self.sample())
        self.previous_sample_time = time.time()

    
