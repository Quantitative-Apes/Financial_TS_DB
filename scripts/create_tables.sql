DROP TABLE klines_5min;
CREATE TABLE klines_1min(
    ticker SYMBOL index,
    open_t TIMESTAMP,
    close_t TIMESTAMP,
    "open" FLOAT,
    high FLOAT,
    low FLOAT,
    "close" FLOAT,
    volume FLOAT,
    qav FLOAT,
    n_trades INT,
    tbbav FLOAT,
    tbqav FLOAT,
    ignore INT)
timestamp(open_t)
PARTITION BY DAY;

-- Per year and ticker, 211mb
-- In total, 1 year 320 tickers: 66gb

-- Once the table above is populated, populate tables for other frequencies
DROP TABLE klines_5min;
CREATE TABLE klines_5min AS(
    SELECT 
        ticker, 
        FIRST(open_t) open_t, 
        last(close_t) close_t, 
        FIRST(open) open, 
        MAX(high) high, 
        MIN(low) low, 
        LAST(close) close, 
        SUM(volume) volume, 
        SUM(qav) qav, 
        SUM(n_trades) n_trades, 
        SUM(tbbav) tbbav, 
        SUM(tbqav) tbqav, 
        SUM(ignore) ignore 
    FROM 'klines_1min' SAMPLE BY 5m
)
TIMESTAMP(open_t)
PARTITION BY DAY;

DROP TABLE klines_1hour;
CREATE TABLE klines_1hour AS(
    SELECT 
        ticker, 
        FIRST(open_t) open_t, 
        last(close_t) close_t, 
        FIRST(open) open, 
        MAX(high) high, 
        MIN(low) low, 
        LAST(close) close, 
        SUM(volume) volume, 
        SUM(qav) qav, 
        SUM(n_trades) n_trades, 
        SUM(tbbav) tbbav, 
        SUM(tbqav) tbqav, 
        SUM(ignore) ignore 
    FROM 'klines_1min' SAMPLE BY 1h
)
TIMESTAMP(open_t)
PARTITION BY DAY;

DROP TABLE klines_1day;
CREATE TABLE klines_1day AS(
    SELECT 
        ticker, 
        FIRST(open_t) open_t, 
        last(close_t) close_t, 
        FIRST(open) open, 
        MAX(high) high, 
        MIN(low) low, 
        LAST(close) close, 
        SUM(volume) volume, 
        SUM(qav) qav, 
        SUM(n_trades) n_trades, 
        SUM(tbbav) tbbav, 
        SUM(tbqav) tbqav, 
        SUM(ignore) ignore 
    FROM 'klines_1min' SAMPLE BY 1d
)
TIMESTAMP(open_t)
PARTITION BY DAY;


-- SAMPLE BY yields 

