class QuantLib:
    def __init__(self):
        pass

    def variance(self,lst):
        """
        Takes in a list of real numbers and returns their variance or 0 if an empty list is provided. 
        """
        if lst is None or lst == []:
            return 0
        mu = 0
        for num in lst:
            if not isinstance(num, (int, float)):
                raise "Expected only real numbers in input list"
            mu += num
        mu = mu/num
        var = 0
        for num in lst:
            var += (num - mu)**2
        var = var/len(lst)
        return var