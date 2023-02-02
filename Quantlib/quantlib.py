class QuantLib:
    def __init__(self):
        pass

    def variance(self,lst):
        """
        Takes in a list of real numbers and returns the population variance or 0 if an empty list is provided. 
        """
        if lst is None or lst == []:
            return 0
        mu = 0
        for num in lst:
            if not isinstance(num, (int, float)):
                raise ValueError("Expected only real numbers in input list")
            mu += num
        mu = mu/len(lst)
        var = 0
        for num in lst:
            var += (num - mu)**2
        var = var/len(lst)
        return var

    def ema(self,data, period, smoothing=2):
        if len(data) < period:
            raise ValueError("Not enough data for calculation!")
    
        if period < 1:
            raise ValueError("Period cannot be negative!")

        if smoothing <= 0:
            raise ValueError("Invalid Smoothing Value (Must be > 0)!")
    
        ema_list = []
    
        k = smoothing / (period + 1)
        ema_list.append(sum(data[:period]) / period)
        for i in range(period, len(data)):
            ema_list.append(data[i] * k + ema_list[-1] * (1 - k))
    
        return ema_list, ema_list[-1]
    
    def sma(self,data, period):
        if len(data) < period:
            raise ValueError("Not enough data for calculation!")

        if period < 1:
            raise ValueError("Period cannot be negative!")

        sma_list = []

        for i in range(len(data) - period + 1):
            sma_list.append(sum(data[i:i+period]) / period)

        return sma_list, sma_list[-1]


