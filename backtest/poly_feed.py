import sys, os
import argparse
import requests
import pprint
from datetime import date, datetime, timezone, timedelta
import csv
from typing import *
from creds import polygon_apikey

class PolygonFeeder():
    '''
        args:
        - start: '2019-01-01'
        - end: '2019-02-01'
        - range: 100
        - timespan: 'minute/hour/day/week/month/quarter/year'
        - multiplier: 1
    '''
    def get_historical_stock(self, ticker: str, **kwargs) -> None:
        print('get historical stock:', ticker, kwargs)
        multiplier = kwargs.get('multiplier', 1)
        timespan = kwargs.get('timespan', 'day')
        if 'range' in kwargs:
            range = int(kwargs['range'])
            start = str(date.today()  - timedelta(days=range + 1))
            end = str(date.today() - timedelta(days=1))
        else:
            start = kwargs.get('start', str(date.today()  - timedelta(days=280)))
            end =  kwargs.get('end', str(date.today() - timedelta(days=1)))
        url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start}/{end}?apiKey={polygon_apikey}&unadjusted=false'
        print(url)
        resp = requests.get(url).json()
        print('result len', len(resp['results']))
        return self.write_historical_stock_to_csv(resp, timespan)

    '''
        write to match backtrader generic csv data feed
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', 6)
    '''
    def write_historical_stock_to_csv(self, resp, timespan):
        ticker, results = resp['ticker'], resp['results']
        first_date = datetime.fromtimestamp(results[0]['t']/1000.0, timezone.utc).date()
        last_date = datetime.fromtimestamp(results[-1]['t']/1000.0, timezone.utc).date()
        print(f'first date: {first_date}, last date: {last_date}')
        path = os.path.dirname(os.path.realpath(__file__))
        file_name = f'{path}/data/{ticker}-{timespan}.csv'
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            for result in results:
                utc_dt = datetime.fromtimestamp(result['t']/1000.0, timezone.utc)
                if timespan == 'minute' or timespan == 'hour':
                    dt = utc_dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    dt = utc_dt.strftime('%Y-%m-%d')
                writer.writerow([dt, result['o'], result['h'], result['l'], result['c'], result['v']])
        return file_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ticker', help='stock name i.e. MSFT')
    parser.add_argument('--polygon')
    parser.add_argument('--range')
    parser.add_argument('--start')
    parser.add_argument('--end')
    parser.add_argument('--timespan')
    parser.add_argument('--multiplier')
    args = vars(parser.parse_args())
    valid_args = {}
    for k, v in args.items():
        if v:
            valid_args[k] = v
    cwd = ''
    PolygonFeeder().get_historical_stock(**valid_args)
