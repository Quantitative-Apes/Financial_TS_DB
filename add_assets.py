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
    tickers = bu.get_tickers(client)[]
    #print(len(tickers), tickers)

    dbh = connect.DBHandler()
    cursor = dbh.get_cursor()
    start_date = '2021-01-01'
    end_date = '2021-01-02'
    print(f'attempting insert for {len(tickers)} tickers')

    for date in pd.date_range(start_date, end_date, freq='d'):
        current_date = date.date()
        daily_df = pd.DataFrame()
        for ticker in tickers:
            try:
                klines_df = bu.get_historical_klines(client, ticker, current_date, current_date+pd.DateOffset(1), interval=bu.Consts.INTERVAL_1MIN)
                klines_df['ticker'] = ticker
                daily_df = pd.concat([daily_df, klines_df])
            except:
                print('Could not fetch data for date', current_date, 'and ticker', ticker)

        daily_df = daily_df.sort_values(by='close_t')
        
        try:
            
            daily_df = daily_df.values.tolist()[:-1] # remove last entry to remove dupes
            print(len(daily_df))
            for row in daily_df:
                # Want: ticker, close_t,"open,high,low,"close",volume,qav,n_trades,tbbav,tbqav,ignore
                to_insert = [
                    row[11],
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
    print('done')
    exit()