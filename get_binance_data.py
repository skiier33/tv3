import pandas as pd
import ccxt
import datetime
import time

exchange = ccxt.binanceus()
symbol = 'BTCUSDT'
timeframe = '1m'
limit = 1000

since = datetime.datetime(2024,1,1,1,1,1)

def format_since(since:datetime)->datetime:

    since = since.strftime("%Y-%m-%d %H:%M:%S")
    since = exchange.parse8601(since)
    return since



since = format_since(since)

def get_data(exchange, symbol, timeframe, since, limit):
    since = since.strftime("%Y-%m-%d %H:%M:%S")
    since = exchange.parse8601(since)

    all_data = []
    while True:

        data = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        if not data:
            break
        all_data += data

        first_date = datetime.datetime.utcfromtimestamp(data[0][0] // 1000).strftime("%Y-%m-%d %H:%M:%S")
        last_date = datetime.datetime.utcfromtimestamp(data[-1][0] // 1000).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Fetched {len(data)} data points from {first_date} to {last_date}")
        since = data[-1][0] + exchange.parse_timeframe(timeframe) * 1000
        time.sleep(0.1)  # Add a small delay to avoid hitting rate limits

    df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    return df

df = get_data(exchange, symbol, timeframe, since, limit)

d
print(data)