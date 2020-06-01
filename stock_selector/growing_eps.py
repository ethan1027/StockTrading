import alpaca_trade_api as tradeapi
from polygon import RESTClient
import pandas as pd
import sys
# POLYGON_KEY = 'AKMSXURYBJ1CHOHYN396'

API_KEY = "PKWFUZFXNLV2J9FAXQIU"
API_SECRET = "Y8F5q3GTRw5nbXiDfmEjGE/PUCvDb/WWzGCZBrbZ"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
ALPHAVANTAGE_KEY = 'MR35347XSCWHHYDA'
alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')
client = RESTClient(API_KEY)

# f = client.reference_stock_financials('AAPL', limit=5, type='Q', sort='-reportPeriod')
# print(f.results[0])

nasdaq = pd.read_csv('nasdaqlisted.txt',delimiter='|')

large_marketcaps = []

for symbol in nasdaq['Symbol']:
    try:
        ticker_details = client.reference_ticker_details(symbol)
        print(ticker_details.marketcap)
        if ticker_details.marketcap > 4000000000:
            large_marketcaps.append(symbol)
    except Exception:
        print(sys.exc_info())
# pd.DataFrame({ symbol: large_marketcaps }).to_csv('large_marketcaps')
print(large_marketcaps)