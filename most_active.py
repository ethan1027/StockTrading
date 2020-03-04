import requests
from datetime import date, timedelta
from joblib import Parallel, delayed
import multiprocessing
import pandas as pd
import statistics

api_key = 'AKMSXURYBJ1CHOHYN396'

class KstockModel:
    def __init__(self, ticker, avg_vol):
        self.ticker = ticker
        self.avg_vol = avg_vol

    def __eq__(self, other):
        return self.active_ratio == other.active_ratio
    
    def __gt__(self, other):
        return self.active_ratio < other.active_ratio

    def __lt__(self, other):
        return self.active_ratio > other.active_ratio

    def __repr__(self):
        current_vol = self.current['v']
        price = self.current['c']
        movement = '⬆️' if self.active_ratio > 0.0 else '⬇️'
        percentage = '{:.1%}'.format(self.active_ratio)
        f_cur_vol = f'{current_vol:,}'
        f_avg_vol = f'{self.avg_vol:,}'
        return f'{self.ticker:<9}|{f_cur_vol:>12} |{f_avg_vol:>12} |{price:>7} | {movement} {percentage}'

def get_stock_details(ticker: str):
    try:
        return requests.get(f'https://api.polygon.io/v1/meta/symbols/{ticker}/company?apiKey={api_key}').json()
    except:
        return None

def get_historical_stock(ticker: str):
    try:
        today = date.today()
        yesterday = str(today - timedelta(days=1))
        three_months_ago = (today - timedelta(days=90))
        return requests.get(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{three_months_ago}/{yesterday}?apiKey={api_key}').json()
    except:
        return None

def get_avg_volume(historical_stock) -> KstockModel:
    volumes = [result['v'] for result in historical_stock['results']]
    avg_vol = int(statistics.mean(volumes))
    return KstockModel(historical_stock['ticker'], avg_vol)

def get_ticker_snapshot(k_stock_model: KstockModel) -> KstockModel:
    snap_shot = requests.get(f'https://api.polygon.io//v2/snapshot/locale/us/markets/stocks/tickers/{k_stock_model.ticker}?apiKey={api_key}').json()
    k_stock_model.current = snap_shot['ticker']['day']
    k_stock_model.active_ratio = k_stock_model.current['v'] / k_stock_model.avg_vol - 1.0
    return k_stock_model

k_tickers = pd.read_csv('test_tickers.csv')
print('tickers count', len(k_tickers.columns))
num_cores = multiprocessing.cpu_count()
print('num of cores', num_cores)
historical_stocks = Parallel(n_jobs=num_cores)(delayed(get_historical_stock)(ticker) for ticker in k_tickers)
avg_volumes = [get_avg_volume(stock) for stock in historical_stocks]
k_stock_models = Parallel(n_jobs=num_cores)(delayed(get_ticker_snapshot)(avg_vol) for avg_vol in avg_volumes)
k_stock_models.sort()
with open('sample.txt', 'w') as f:
    f.write('ticker	 |     cur vol |     avg vol |  price |   move %\n')
    f.write('--------|-------------|-------------|--------|----------\n')
    for m in k_stock_models:
        f.write(repr(m) + '\n')

