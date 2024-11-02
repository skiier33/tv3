import pandas as pd
import ccxt
import datetime
import time
import plotly.graph_objects as go
import numpy as np
import os
import pathlib
# from DataClass import TimeFrameData


def update_data(csv_path:pathlib, timeframe):
    """
    :param csv_path: The directory path where the CSV file is located
    :param timeframe: The timeframe for which new data needs to be fetched
    :return: None
    """
    os.chdir(csv_path)

    old_data = read_binance_csv(csv_path)
    since = old_data.index[-1]

    new_data = get_data(since=since, timeframe=timeframe)
    new_csv = pd.concat([old_data, new_data])
    new_csv.to_csv(timeframe+'.csv')

######################################################################################################################

exchange = ccxt.binanceus()
symbol = 'BTCUSDT'
timeframe = '1m'
limit = 1000
# since = datetime.datetime(year=year, month=month, day=day, hour=1, minute=1, second=1)
since = datetime.datetime(2022,1,1,1,1,1)

def get_data(since:datetime.datetime,  timeframe:str, symbol='BTCUSDT', exchange=ccxt.binanceus(), limit:int=1000)->pd.DataFrame:
    """
    :param since: The starting datetime for fetching OHLCV data.
    :param timeframe: The granularity of the OHLCV data (e.g., '1m' for 1 minute).
    :param symbol: The trading pair symbol (default is 'BTCUSDT').
    :param exchange: The exchange instance from which to fetch the data (default is ccxt.binanceus()).
    :param limit: The maximum number of data points to fetch in one API call (default is 1000).
    :return: A DataFrame containing the timestamp, open, high, low, close, and volume of the fetched OHLCV data.
    """
    since = since.strftime("%Y-%m-%d %H:%M:%S")
    since = exchange.parse8601(since)
    timeframe = timeframe
    symbol = symbol

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
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df.set_index('timestamp', inplace=True)

    return df

######################################################################################################################

def read_binance_csv(file)->pd.DataFrame:
    """
    :param file: The path to the Binance CSV file to be read.
    :type file: str
    :return: A pandas DataFrame with the timestamp column as the index and in UTC.
    :rtype: pd.DataFrame
    """
    df = pd.read_csv(file)
    df.timestamp = pd.to_datetime(df.timestamp, utc=True)
    df.index = df.timestamp
    df.drop(columns=['timestamp'], inplace=True)

    return df

###########################################################

def get_hlines(hold)->pd.DataFrame:
    """
    :param hold: Input data to be transformed into a DataFrame. Expected to be a format compatible with pandas DataFrame creation.
    :return: A pandas DataFrame with renamed and reset index columns, including additional calculated columns 'x1', 'y1'.
    """
    hlines = pd.DataFrame(hold)
    hlines['x1'] = hlines.index[-1]
    hlines['y1'] = hlines[0]
    hlines.index.name='x0'
    hlines = hlines.reset_index()

    return hlines.rename(columns={0:'y0'})

#####################################################################################

def plot_df(df):
    """
    :param df: DataFrame containing the stock prices with columns 'open', 'high', 'low', 'close' and an index for dates.
    :return: A Plotly Figure object with a candlestick chart representing the stock prices.
    """
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])], layout=go.Layout())
    fig.update_layout(xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price', template="plotly_dark")
    fig.update_traces(increasing_line_color= 'white', selector = dict(type='candlestick'))
    fig.update_traces(decreasing_line_color= 'cyan', selector = dict(type='candlestick'))

    return fig


def add_hold_lines(fig, holds)->go.Figure:
    """
    :param fig: Plotly graph object (go.Figure) to which lines will be added.
    :param holds: pandas DataFrame containing the coordinates for the lines. Each row should have four values: x0, y0, x1, y1.
    :return: Updated Plotly figure with added lines.
    """
    fig = fig

    for row in holds.index:
        x0, y0, x1, y1 = holds.loc[row].values
        fig.add_shape(type='line', line=dict(color='red'), label=dict(text=y1, textposition='end', padding=0, font=dict(size=10),xanchor='right', yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

    return fig



def test_holds(holds:pd.Series, tests:pd.Series) -> pd.DataFrame:
    """

    :param holds: Series of hold levels to test
    :param tests: Timeframe of data used to test
    :return: all the hold levels that passed the test
    """
  #  Test hold levels based on mask usually series.isin(test
    total = len(holds)
    mask = holds.isin(tests)

    ix_drop = holds[mask].index
    dropped = f'Drop: {len(ix_drop)} '

    untested = holds.drop(labels=ix_drop)
    print(f'Total Holds:{total}  Dropped:{dropped}  Untested:{len(untested)}\n')

    return untested


def add_timeframe(fig, df):
    fig = fig
    df=df
    fig.add_trace(go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close']))

    return fig


def test_long_hold(longs_df, test_df):
    '''
    plug in untested longs or shorts to test with all lower timeframes
    :param untested_hold:
    :return: untested levels
    '''
    longs = longs_df
    test = test_df

    # for tf in [ '15m.csv', '5m.csv', '3m.csv', '1m.csv']:
    #
    #     print(f' Testing with {tf}')
    #
    #     csv_path = csv_folder.joinpath(tf)

    test = test.loc[test.index > longs.index[0]]


    untested = test_holds(longs, test.low)


    return untested


def download_csv_for_timeframes(symbol: str, timeframes: list, since: datetime.datetime, exchange=ccxt.binanceus(),
                                directory: str = './csv_data') -> None:
    """
    Downloads CSV data for multiple timeframes and saves them to a specified directory.

    :param symbol: The trading pair symbol.
    :param timeframes: List of timeframes to download data for.
    :param since: The starting datetime for fetching OHLCV data.
    :param exchange: The exchange instance from which to fetch the data (default is ccxt.binanceus()).
    :param directory: Directory to save the CSV files.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    for timeframe in timeframes:
        df = get_data(since, timeframe, symbol, exchange)
        filename = f"{symbol}_{timeframe}.csv"
        filepath = os.path.join(directory, filename)
        df.to_csv(filepath)
        print(f"Data for {timeframe} timeframe saved to: {filepath}")


# def test_short_hold(untested_hold):
#     '''
#     plug in untested longs or shorts to test with all lower timeframes
#     :param untested_hold:
#     :return: untested levels
#     '''
#     untested = untested_hold.shorts
#
#     for tf in ['15m.csv', '5m.csv', '3m.csv', '1m.csv']:
#         print('f Testing with {tf}')
#     test = TimeFrameData(read_binance_csv(p.joinpath(tf)))
#     test = test.loc[test.index > untested.index[0]]
#     untested = test_holds(untested, test.df.high)
#
#     return untested_shorts