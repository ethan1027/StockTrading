import backtrader as bt

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.atr = bt.ind.AverageTrueRange()
        
    def next(self):
        print(self.atr.atr[0])