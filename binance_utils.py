from dotenv import load_dotenv
import os
import binance
import pandas as pd
from tqdm import tqdm

class Consts:
    INTERVAL_1MIN = binance.Client.KLINE_INTERVAL_1MINUTE
    INTERVAL_5MIN = binance.Client.KLINE_INTERVAL_5MINUTE

    kline_colnames = [
        'open_t',
        'open',
        'high',
        'low',
        'close',
        'volume',
        'close_t',
        'qav', # quote asset volume
        'n_trades',
        'tbbav', # taker buy base asset volume,
        'tbqav', # taker buy quote asset volume,
        'ignore',
    ]
    binance_t_to_pd_t = {
        binance.Client.KLINE_INTERVAL_1MINUTE : '1min',
        binance.Client.KLINE_INTERVAL_5MINUTE : '5min',
        binance.Client.KLINE_INTERVAL_15MINUTE: '15min',
        binance.Client.KLINE_INTERVAL_30MINUTE: '30min',
        binance.Client.KLINE_INTERVAL_1HOUR: '1hour',
        binance.Client.KLINE_INTERVAL_1DAY: 'D',
    }

def get_credentials():
    """get Binance credentials from environment"""
    load_dotenv()
    BINANCE_KEY = os.getenv('BIN_KEY')
    BINANCE_SECRET = os.getenv('BIN_SECRET')

    return BINANCE_KEY, BINANCE_SECRET

def get_client(key:str, secret:str):
    """get binance Client object"""
    return binance.Client(key, secret)

def get_tickers(client:binance.Client, desired_base:str='BUSD'):
    """get all pairs available, with a given base currency"""
    tickers = client.get_ticker()
    df = pd.DataFrame(tickers)
    ticker_ids = [ticker['symbol'] for ticker in tickers if ticker['symbol'][-4:] == desired_base] # use BUSD as base currency
    ticker_ids = [ticker for ticker in ticker_ids if "BEAR" not in ticker] # no weird derivatives
    ticker_ids = [ticker for ticker in ticker_ids if "BULL" not in ticker] # no weird derivatives
    return ticker_ids

def date_range(start:str, end:str, freq, step=500):
    """generator to iterate through a given date range. Used to fetch historical klines"""
    r = pd.date_range(start, end, freq=freq)
    for i in range(0, len(r), step):
        first_idx = i+1 if i!=0 else 0
        yield r[first_idx], r[min(i+step, len(r)-1)]

def get_historical_klines(client:binance.Client, ticker:str, start_date:str, end_date:str, interval=binance.Client.KLINE_INTERVAL_1MINUTE):
    """get kline data as DataFrame for one ticker"""

    klines = pd.DataFrame()
    for start_t, end_t in tqdm(date_range(start=start_date, end=end_date, freq=Consts.binance_t_to_pd_t[interval], step=500)):
        new_klines = pd.DataFrame(client.get_historical_klines(ticker, interval, str(start_t), str(end_t)))
        new_klines.columns = Consts.kline_colnames
        klines = pd.concat(
            [klines, 
            new_klines],
            axis=0
        )
    klines.open_t = pd.to_datetime(klines.open_t, unit='ms')
    klines.close_t = pd.to_datetime(klines.close_t, unit='ms')
    klines = klines.set_index('open_t')
    return klines

if __name__ == '__main__':
    key, secret = get_credentials()
    client = get_client(key, secret)
    #tickers = get_tickers(client)
    klines = get_historical_klines(client, 'BTCBUSD', '2021-01-01', '2021-01-02', interval=binance.Client.KLINE_INTERVAL_1MINUTE)
    print(klines)
    #print(list(date_range('2021-01-01', '2021-01-02', '1min', 500)))