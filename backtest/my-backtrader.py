import backtrader as bt
from datetime import datetime 

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    
    data = bt.feeds.YahooFinanceData(dataname='ZOOM', fromdate=datetime(2018, 11, 30))
    cerebro.adddata(data)
    cerebro.run()
    cerebro.plot(style='candle')
