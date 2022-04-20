import alpaca_trade_api as tradeapi
import threading
import time
import datetime
from alpha_vantage.techindicators import TechIndicators
from polygon import RESTClient
import pandas as pd
import sys

API_KEY = "*"
API_SECRET = "*"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
ALPHAVANTAGE_KEY = '*'
POLYGON_KEY = '*'

alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')
ti = TechIndicators(key=ALPHAVANTAGE_KEY, output_format='pandas')
symbol = 'BAC'
while True:
    if alpaca.get_clock().is_open:
        try:
            print(alpaca.get_clock())
            print('position', alpaca.list_positions())
            fast_series, _ = ti.get_wma(symbol, interval='15min', time_period=4)
            slow_series, _ = ti.get_wma(symbol, interval='15min', time_period=32)
            fast = fast_series.iloc[-1]['WMA']
            slow = slow_series.iloc[-1]['WMA']
            print(f'fast: {fast}, slow: {slow}')
            if len(alpaca.list_positions()) == 0:
                if  fast > slow:
                    equity = 5000 + int(float(alpaca.get_account().equity)) - 100000
                    price = alpaca.polygon.last_trade(symbol).price
                    qty = equity // price - 1
                    if qty > 0:
                        buy_order = alpaca.submit_order(
                            symbol=symbol,
                            qty=qty,
                            side='buy',
                            type='market',
                            time_in_force='day'
                        )
                        print('BUY', buy_order)
            elif fast < slow:
                sell_order = alpaca.submit_order(
                    symbol=symbol,
                    qty=alpaca.get_position(symbol).qty,
                    side='sell',
                    type='market',
                    time_in_force='day'
                )
                print('SELL', sell_order)
        except Exception:
            print(sys.exc_info())
        time.sleep(60*15)
    else:
        time.sleep(60)
    print("\n\n")