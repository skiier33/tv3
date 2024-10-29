import ccxt
import datetime
import time
import pandas as pd


def get_historical_klines(exchange, symbol, timeframe, since, limit):
    ohlcv_data = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    return ohlcv_data


def get_all_historical_klines(exchange, symbol, timeframe):
    all_data = []
    since = exchange.parse8601(
        "2017-01-01T00:00:00Z")  # Set the start time to the earliest available date (January 1st, 2017)
    limit = 1000
    while True:
        data = get_historical_klines(exchange, symbol, timeframe, since, limit)
        if not data:
            break
        all_data += data
        first_date = datetime.datetime.utcfromtimestamp(data[0][0] // 1000).strftime("%Y-%m-%d %H:%M:%S")
        last_date = datetime.datetime.utcfromtimestamp(data[-1][0] // 1000).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Fetched {len(data)} data points from {first_date} to {last_date}")
        since = data[-1][0] + exchange.parse_timeframe(timeframe) * 1000
        time.sleep(0.1)  # Add a small delay to avoid hitting rate limits

    df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df.set_index('timestamp', inplace=True)
    return df


binance_us = ccxt.binanceus()

symbol = "ETH/USD"
timeframe = "1m"  # 1 minute interval

historical_data = get_all_historical_klines(binance_us, symbol, timeframe)

# Save the data to a CSV file
# historical_data.to_csv('historical_data.csv')

# Print the first few rows of the dataframe
print(historical_data.head())