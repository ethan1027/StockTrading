import backtrader as bt
from datetime import datetime
from .strategy import SmaCross

def run():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    data = bt.feeds.GenericCSVData(dataname='YHOO', fromdate=datetime(2016, 1, 1), todate=datetime(2016, 2, 1))
    # cerebro.adddata(data)
    # cerebro.run()
    # cerebro.plot(start=datetime(2019, 1, 1), end=datetime(2019, 12, 1))
