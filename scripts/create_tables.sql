CREATE TABLE assets(
    ticker SYMBOL,
    type SYMBOL
);

CREATE TABLE klines_1min(
    ticker SYMBOL index,
    close_t TIMESTAMP,
    "open" FLOAT,
    high FLOAT,
    low FLOAT,
    "close" FLOAT,
    volume INT,
    qav FLOAT,
    n_trades INT,
    tbbav FLOAT,
    tbqav FLOAT,
    ignore INT)
timestamp(close_t)
PARTITION BY DAY;