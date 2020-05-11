import backtrader as bt

class BaseMaStrategy(bt.Strategy):
    def next(self):
        if not self.position:
            limit = self.broker.getvalue()
            buy_size = limit // self.data.close[0] - 1
            if self.crossover > 0:
                self.buy(size=buy_size)
        elif self.crossover < 0:
            self.sell(size=self.position.size)
    
    @staticmethod
    def setMovingRange(fast, slow):
        BaseMaStrategy.params.fast = fast
        BaseMaStrategy.params.slow = slow

class AmaStrategy(BaseMaStrategy):
    def __init__(self):
        ama1 = bt.ind.AdaptiveMovingAverage(period=super().params.fast)
        ama2 = bt.ind.AdaptiveMovingAverage(period=super().params.slow)
        self.crossover = bt.ind.CrossOver(ama1, ama2)
        

class WmaStrategy(BaseMaStrategy):
    def __init__(self):
        wma1 = bt.ind.WeightedMovingAverage(period=super().params.fast)
        wma2 = bt.ind.WeightedMovingAverage(period=super().params.slow)
        self.crossover = bt.ind.CrossOver(wma1, wma2)

class EmaStrategy(BaseMaStrategy):
    def __init__(self):
        ema1 = bt.ind.ExponentialMovingAverage(period=super().params.fast)
        ema2 = bt.ind.ExponentialMovingAverage(period=super().params.slow)
        self.crossover = bt.ind.CrossOver(ema1, ema2)



