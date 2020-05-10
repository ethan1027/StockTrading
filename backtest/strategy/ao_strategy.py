import backtrader as bt

class AOStrategy(bt.Strategy):
    def __init__(self):
        self.ao = bt.ind.AwesomeOscillator()

    def next(self):
        print(self.ao[0])