import requests
import pprint
from datetime import date, datetime, timezone, timedelta
import csv
from typing import *

api_key = 'AKMSXURYBJ1CHOHYN396'

def get_historical_stock(ticker: str, **kwargs):
    start = kwargs.get('start', str(date.today()  - timedelta(days=90)))
    end =  kwargs.get('end', str(date.today() - timedelta(days=1)))
    print(f'execute in time range start={start}, end={end}')
    try:
        return requests.get(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}?apiKey={api_key}').json()
    except:
        raise Exception('unable to get data from Polygon')

def write_historical_stock_to_csv(resp):
    ticker, results = resp['ticker'], resp['results']
    first_date = datetime.fromtimestamp(results[0]['t']/1000.0, timezone.utc).date()
    last_date = datetime.fromtimestamp(results[-1]['t']/1000.0, timezone.utc).date()
    print(first_date)
    print(last_date)
    with open(f'{ticker}_{first_date}_{last_date}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # write to match backtrader generic csv data feed
        # ('datetime', 0),
        # ('time', -1),
        # ('open', 1),
        # ('high', 2),
        # ('low', 3),
        # ('close', 4),
        # ('volume', 5),
        # ('openinterest', 6)
        for result in results:
            dt = datetime.fromtimestamp(result['t']/1000.0, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([dt, result['o'], result['h'], result['l'], result['c'], result['v']])

resp = get_historical_stock('MSFT')
write_historical_stock_to_csv(resp)