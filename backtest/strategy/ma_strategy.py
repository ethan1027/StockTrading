import backtrader as bt

class BaseMaStrategy(bt.Strategy):
    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy(size=20)

        elif self.crossover < 0:
            print(self.crossover)
            self.sell(size=20)

class BaseAmaStrategy(BaseMaStrategy):
    def __init__(self):
        sma1 = bt.ind.AdaptiveMovingAverage(period=self.params.short)
        sma2 = bt.ind.AdaptiveMovingAverage(period=self.params.long)
        bt.ind
        self.crossover = bt.ind.CrossOver(sma1, sma2)

class AmaStrategy1(BaseAmaStrategy):
    params = dict(short=3, long=15)

class AmaStrategy2(BaseAmaStrategy):
    params = dict(short=10, long=30)

class AmaStrategy2(BaseAmaStrategy):
    params = dict(short=9, long=30)

class BaseWmaStrategy(BaseMaStrategy):
    def __init__(self):
        adx1 = bt.ind.WeightedMovingAverage(period=self.params.short)
        adx2 = bt.ind.WeightedMovingAverage(period=self.params.long)
        bt.ind.CrossOver(adx1, adx2)

