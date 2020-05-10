import alpaca_trade_api as tradeapi
import threading
import time
import datetime
from alpha_vantage.techindicators import TechIndicators
from polygon import RESTClient
import pandas as pd

API_KEY = "PKWFUZFXNLV2J9FAXQIU"
API_SECRET = "Y8F5q3GTRw5nbXiDfmEjGE/PUCvDb/WWzGCZBrbZ"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
ALPHAVANTAGE_KEY = 'MR35347XSCWHHYDA'
POLYGON_KEY = 'AKMSXURYBJ1CHOHYN396'

alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')
ti = TechIndicators(key=ALPHAVANTAGE_KEY, output_format='pandas')
symbol = 'RP'
print(alpaca.polygon.last_trade(symbol).price)
while False:
    print(alpaca.list_positions())
    if alpaca.get_clock().is_open:
        fast, _ = ti.get_wma(symbol, interval='15min', time_period=4)
        slow, _ = ti.get_wma(symbol, interval='15min', time_period=32)
        if len(alpaca.list_positions()) == 0:
            equity = 5000 + alpaca.get_account().equity - 100000
            price = alpaca.polygon.last_trade(symbol).price
            qty = equity // price - 1
            if fast > slow:
                alpaca.submit_order(
                    symbol=symbol,
                    qty=qty,
                    side='buy',
                    type='market',
                    time_in_force='day'
                )
        elif fast < slow:
            qty = alpaca.get_position(symbol).qty
            alpaca.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='day'
            )
        time.sleep(60*15)
    else:
        time.sleep(60)