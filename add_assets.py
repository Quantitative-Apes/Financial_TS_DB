import connect
import binance_utils as bu
import pandas as pd

def insert_asset(ticker:str, type:str, dbh:connect.DBHandler):
    cursor = dbh.get_cursor()
    
    cursor.execute(f"""
    INSERT INTO assets VALUES (%s, %s);
    """, (ticker, type))

if __name__ == '__main__':

    key, secret = bu.get_credentials()
    client = bu.get_client(key, secret)
    tickers = bu.get_tickers(client)[:2]
    #print(len(tickers), tickers)

    dbh = connect.DBHandler()
    cursor = dbh.get_cursor()
    start_date = '2021-01-01'
    end_date = '2022-12-31'
    print(f'attempting insert for {len(tickers)} tickers')
    for ticker in tickers:
        print(ticker)
        try:
            insert_asset(ticker, "crypto", dbh)
            klines_df = bu.get_historical_klines(client, 'VETBUSD', start_date, end_date, interval=bu.Consts.INTERVAL_1MIN)
            klines_df = klines_df.values.tolist()
            for row in klines_df:
                # Want: ticker, close_t,"open,high,low,"close",volume,qav,n_trades,tbbav,tbqav,ignore
                to_insert = [
                    ticker,
                    row[5],
                    float(row[0]),
                    float(row[1]),
                    float(row[2]),
                    float(row[3]),
                    float(row[4]),
                    float(row[6]),
                    int(row[7]),
                    float(row[8]),
                    float(row[9]),
                    int(row[10]),
                ]
                cursor.execute(f"INSERT INTO klines_1min VALUES({('%s,'*12)[:-1]});", to_insert)
                dbh.commit()
        except Exception as e:
            print(ticker, 'failed. error:', e)
        
        #insert_df(klines_df, 'klines_1m', dbh)
    #insert_df(klines_df, 'klines_1m')