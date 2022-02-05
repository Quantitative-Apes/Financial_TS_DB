import connect
import binance_utils as bu
import pandas as pd

if __name__ == '__main__':

    key, secret = bu.get_credentials()
    client = bu.get_client(key, secret)
    tickers = bu.get_tickers(client)
    print(tickers)
    tickers = tickers[:1]

    dbh = connect.DBHandler()
    cursor = dbh.get_cursor()
    start_date = '2021-01-01'
    end_date = '2021-12-31'
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

        daily_df = daily_df.sort_values(by='open_t')
        
        try:
            
            daily_df = daily_df.values.tolist()[:-1] # remove last entry to remove dupes
            print(len(daily_df))
            for row in daily_df:
                # Want: ticker, open_t, close_t,"open,high,low,"close",volume,qav,n_trades,tbbav,tbqav,ignore
                to_insert = [
                    row[12],
                    row[0],
                    row[6],
                    float(row[1]),
                    float(row[2]),
                    float(row[3]),
                    float(row[4]),
                    float(row[5]),
                    float(row[7]),
                    int(row[8]),
                    float(row[9]),
                    float(row[10]),
                    int(row[11]),
                ]
                #print(to_insert)
                cursor.execute(f"INSERT INTO klines_1min VALUES({('%s,'*13)[:-1]});", to_insert)
                dbh.commit()
        except Exception as e:
            print(ticker, 'failed. error:', e)
        
    print('done')
    exit()