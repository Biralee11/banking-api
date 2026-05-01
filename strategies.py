class SimpleInterestStrategy():
    def __eq__(self, other):
        return type(self) == type(other)
    
    def calculate(self, balance, rate, periods=1):
        balance = balance + (balance * rate)
        return balance

class CompoundInterestStrategy():
    def __eq__(self, other):
        return type(self) == type(other)
    
    def calculate(self, balance, rate, periods):
        balance = balance * ((1 + rate) ** periods)
        return balance