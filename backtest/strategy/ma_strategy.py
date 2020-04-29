import backtrader as bt

class BaseMaStrategy(bt.Strategy):
    def next(self):
        if not self.position:
            if self.crossover > 0:
                print('buy', self.data.low[0], self.sma[0])
                self.buy(size=20)

        elif self.crossover < 0:
            print(self.crossover)
            print('sell', self.data.high[0], self.sma[0])
            self.sell(size=20)

class BaseAmaStrategy(BaseMaStrategy):
    def __init__(self):
        sma1 = bt.ind.AdaptiveMovingAverage(period=self.params.pfast)
        sma2 = bt.ind.AdaptiveMovingAverage(period=self.params.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        self.sma = sma1
        rsi1 = bt.ind.RSI(period=10)
        rsi2 = bt.ind.RSI(period=3)
        bt.ind.CrossOver(rsi1, rsi2)
        adx1 = bt.ind.AverageDirectionalMovementIndex(period=10)
        adx2 = bt.ind.AverageDirectionalMovementIndex(period=3)
        bt.ind.CrossOver(adx1, adx2)

class AmaStrategy1(BaseAmaStrategy):
    params = dict(
        pfast=3,
        pslow=15
    )
class AmaStrategy2(BaseAmaStrategy):
    params = dict(
        pfast=10,
        pslow=30
    )

