from backtest import trader
import sys

try:
    trader.run(sys.argv[1])
except:
    raise Exception('request ticker, i.e. python main.py MSFT')