from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from creds import alphavantage_apikey


class AlphaFeeder:
    def __init__(self):
        self.ts = TimeSeries(key=alphavantage_apikey, output_format='pandas')
    
    def get_stock(self, symbol: str):
        data1, md1 = self.ts.get_intraday(symbol, interval='15min',outputsize='full')
        data2, md2 = self.ts.get_intraday(symbol, interval='60min',outputsize='full')
        data3, md3 = self.ts.get_daily(symbol)
        df1 = pd.DataFrame(data1).iloc[::-1]
        df2= pd.DataFrame(data2).iloc[:220].iloc[::-1]
        df3 = pd.DataFrame(data3).iloc[:30].iloc[::-1]
        print(df1)
        print(df2)
        print(df3)
        return ((df1, md1), (df2, md2), (df3, md3))