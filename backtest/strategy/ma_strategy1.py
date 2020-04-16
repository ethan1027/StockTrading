import backtrader as bt

class MaStrategy1(bt.Strategy):
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )
    def __init__(self):
        sma1 = bt.ind.AdaptiveMovingAverage(period=self.params.pfast)
        sma2 = bt.ind.AdaptiveMovingAverage(period=self.params.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        self.sma = sma1

    def next(self):
        if not self.position:
            if self.crossover > 0:
                print('buy', self.data.low[0], self.sma[0])
                self.buy(size=20)

        elif self.crossover < 0:
            print('sell', self.data.high[0], self.sma[0])
            self.sell(size=20)