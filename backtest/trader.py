import backtrader as bt
from datetime import datetime
from .strategy.ma_strategy1 import MaStrategy1
from .strategy.ma_strategy2 import MaStrategy2
from .strategy.ma_strategy3 import MaStrategy3
from .strategy.ma_strategy4 import MaStrategy4
from .strategy.ma_strategy5 import MaStrategy5


def run(ticker: str):
    cerebro = bt.Cerebro()
    print(cerebro.getbroker().getvalue())
    data = bt.feeds.GenericCSVData(dataname=f'backtest/data/{ticker}.csv',
    dtformat=('%Y-%m-%d'),
    datetime=0,
    high=1,
    low=2,
    open=3,
    close=4,
    volume=5,
    openinterest=-1)
    cerebro.adddata(data)
    cerebro.addstrategy(MaStrategy2)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
    strats = cerebro.run()
    print(cerebro.getbroker().getvalue())
    print(len(strats))
    print(strats[0].analyzers.mysharpe.get_analysis())
    cerebro.plot(style='candle')