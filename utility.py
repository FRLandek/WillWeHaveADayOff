

class utility:
    
    """Loops through list and returns the average of list contents
    Args:
        list
    Returns:
        avg (float)"""
    def getAvg(self, list):
        avg = 0.0
        for i in list:
            avg += i
        return avg
    
    """Loops through list and returns the sum of list contents
    Args:
        list
    Returns:
        sum (float)"""
    def getSum(self, list):
        sum = 0.0
        for i in list:
            sum += i
        return sum
    
    """Loops through list and returns the minimum/maximum value of list contents
    Args:
        type (boolean): true = returns max, false = returns min
        list
    Returns:
        max (float)"""
    def getMax(self, type, list):
        max = 0.0
        if type == True:
            for i in list:
                if i > max:
                    max = i
        else:
            for i in list:
                if i < max:
                    max = i
        return max
