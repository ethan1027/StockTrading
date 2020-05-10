import backtrader as bt
from datetime import datetime
from .datafeed import * 
from .strategy.ma_strategy import *
from .strategy.ao_strategy import *


def run(ticker: str, timespan: str, range: int, reuse_data: bool):
    strats = [AOStrategy, AmaStrategy1]
    if reuse_data:
        path = os.path.dirname(os.path.realpath(__file__))
        file_name = f'{path}/data/{ticker}-{timespan}.csv'
    else:
        file_name = get_historical_stock(ticker, range=range, timespan=timespan)
    cerebro = bt.Cerebro()
    print(cerebro.getbroker().getvalue())
    data = bt.feeds.GenericCSVData(dataname=f'{file_name}',
        dtformat=('%Y-%m-%d %H:%M:%S'),
        datetime=0,
        high=1,
        low=2,
        open=3,
        close=4,
        volume=5,
        openinterest=-1)
    cerebro.adddata(data)
    cerebro.addstrategy(AOStrategy)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
    strats = cerebro.run()
    print(cerebro.getbroker().getvalue())
    print(len(strats))
    print(strats[0].analyzers.mysharpe.get_analysis())
    cerebro.plot(style='candle')

