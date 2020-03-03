import backtrader as bt
from datetime import datetime 
class TestStrategy(bt.Strategy):
    def __init__(self):
        self.dataopen = self.datas[0].open

    def next(self):
        print(self.dataopen, self.datas[0].datetime.date(0))

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    data = bt.feeds.YahooFinanceData(dataname='MSFT', fromdate=datetime(2018, 11, 30), todate=datetime(2018, 12, 30))
    cerebro.adddata(data)
    cerebro.run()
    cerebro.plot(style='candle')
