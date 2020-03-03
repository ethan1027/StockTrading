import requests
from datetime import date, timedelta
from joblib import Parallel, delayed
import multiprocessing
import pandas as pd

def get_stock_details(ticker: str):
    try:
        return requests.get(f'https://api.polygon.io/v1/meta/symbols/{ticker}/company?apiKey={api_key}').json()
    except:
        return None

def get_aggregated_volume(ticker: str):
    try:
        today = date.today()
        yesterday = str(today - timedelta(days=1))
        three_months_ago = (today - timedelta(days=90))
        return requests.get(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/2/day/{three_months_ago}/{yesterday}?apiKey={api_key}').json()
    except:
        return None

api_key = 'AKMSXURYBJ1CHOHYN396'

k_tickers = pd.read_csv('k_tickers.csv')
print('tickers count', len(k_tickers.columns))
num_cores = multiprocessing.cpu_count()
print('num of cores', num_cores)
results = Parallel(n_jobs=num_cores)(delayed(get_aggregated_volume)(ticker) for ticker in k_tickers)
print(results[0])
