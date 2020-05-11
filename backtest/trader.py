import backtrader as bt
from datetime import datetime
from .poly_feed import PolygonFeeder
from .alpha_feed import AlphaFeeder
from .strategy.ma_strategy import *
from .strategy.ao_strategy import *
from .summary import Summary


def run(ticker: str, reuse_data: bool):
    data_list = AlphaFeeder().get_stock(ticker)
    datafeed_list = [(get_datafeed(data), metadata) for data, metadata in data_list]
    strategies = [WmaStrategy, EmaStrategy]
    results = []
    
    for datafeed, metadata in datafeed_list:
        for strategy in strategies:
            for fast in range(3, 9):
                for slow in range(20, 41, 2):
                    try:
                        result = run_cerebro(datafeed, strategy, fast, slow, metadata)
                        results.append(result)
                    except:
                        print('error with', strategy.__name__, fast, slow)
            
    results.sort(key=lambda s: s.get_brokerval())
    for r in results:
        print(r)
    best_strategy = results[-1]
    run_cerebro(best_strategy.data, best_strategy.strategy, best_strategy.fast, best_strategy.slow, best_strategy.metadata, True)
    

def run_cerebro(data, strategy, fast, slow, metadata, plot=False) -> Summary:
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name='time_drawdown')
    cerebro.getbroker().set_cash(5000)
    BaseMaStrategy.setMovingRange(fast, slow)
    cerebro.addstrategy(strategy)
    run_strats = cerebro.run()
    if plot:
        cerebro.plot(style='candle')
    return Summary(cerebro, strategy, run_strats[0], data, metadata).slow(slow).fast(fast)


def get_datafeed(data):
    return bt.feeds.PandasDirectData( dataname=data,
    datetime=0,
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
    openinterest=-1)



