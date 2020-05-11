import backtrader as bt

class AOStrategy(bt.Strategy):
    def __init__(self):
        self.ao = bt.ind.AwesomeOscillator()
        self.prev_ao = 1
        self.bought = False

    def next(self):
        if self.prev_ao <= 0 and self.ao[0] > 0:
            order = self.buy(unit=10)
            self.bought = True
        elif self.bought and self.prev_ao > 0 and self.ao[0] < self.prev_ao:
            self.sell(unit=10)
            self.bought = False
        self.prev_ao = self.ao[0] 