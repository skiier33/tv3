

import pandas as pd
import plotly.graph_objects as go

def parse_csv(file, nrows=100)->pd.DataFrame:
    file = file
    nrows = nrows
    df = pd.read_csv(file, nrows=nrows)
    df.time = pd.to_datetime(df.time, unit='s')
    df.index = df.time

    return df



def plot(df, name=None)->go.Figure:
    fig = go.Figure(data=[ go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])], layout=go.Layout())
    fig.update_layout(title=name, xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price', template="plotly_dark")
    fig.update_layout(autosize=True, width=1600, height=600)
    fig.update_traces(increasing_line_color='white', selector=dict(type='candlestick'))
    fig.update_traces(decreasing_line_color='blue', selector=dict(type='candlestick'))

    return fig
#
#
# def get_hold_indexs(self) -> None:
# def TestCandle(int_test, n_test):
#     """
#     """
#     pass
#
#
# def get_untested(int_hold, n_hold, int_test, n_test):
#     """
#     """
#     hc = HoldCandle(int_hold, n_hold)
#     TestCandle(int_test, n_test)
#
#
#
# # def test_holds(holds:pd.Series, tests:pd.Series, func:bool, hold=None, longs=None, total=None) -> pd.DataFrame:
# #     # """
# #     Test hold levels based on mask usually series.isin(test
# #
# #     mask = func
#
#     ix_drop = holds[mask].index
#     dropped = f'Drop: {len(ix_drop)} '
#
#     untested = holds.drop(labels=ix_drop)
#     print(f'Total Holds:{total}  Dropped:{dropped}  Untested:{len(untested)}\n')
#
#     return untested


# def test_range_of_data(reader, range_duration:datetime.timedelta='3D', test_interval:datetime.timedelta='1H'):
#
#     range_start = datetime.datetime.now()-range_duration
#
#     for interval_testing in intervals:
#         n_bars =  range_duration/test_interval
#         timeframe = TimeFrame(reader.test_interval)
#
# def test_range_of_data(reader, hold_interval):
#
#     test_inters = int_df.intervals[int_df.intervals < hold interval]
#
#     for interval_testing in intervals:
#         n_bars =  range_duration/test_interval
#         timeframe = TimeFrame(reader.test_interval)
