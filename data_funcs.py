

import pandas as pd
import plotly.graph_objects as go
import numpy as np


######################################################################################################################

def parse_csv(file)->pd.DataFrame:
    df = pd.read_csv(file)
    df.time = pd.to_datetime(df.time, unit='s')
    df.index = df.time

    return df


######################################################################################################################

###########################################################


def get_hold_ixs(df: pd.DataFrame) -> dict:

    df['up_down'] = np.sign(df.close - df.open)
    levels = dict(longs=dict(frontside=[], backside=[]),
                  shorts=dict(frontside=[], backside=[]))

    for time in df.index[:-4]:
        sl = slice(time, time + 3 * (df.index[1] - df.index[0]))
        chunk = df.loc[sl]

        if all(chunk['up_down'] ==  [1, 1, -1, -1]):
            levels['shorts']['backside'].append(chunk.index[0])
            levels['shorts']['frontside'].append(chunk.index[1])

        elif all(chunk['up_down'] ==  [-1,-1, 1, 1]):
            levels['longs']['backside'].append(chunk.index[0])
            levels['longs']['frontside'].append(chunk.index[1])

    return levels

#####################################################################################

# def get_hlines(self)->pd.DataFrame:
#
#     long_hlines = pd.DataFrame(self.longs)
#     long_hlines['x1'] = self.df.index[-1]
#     long_hlines['y1'] = long_hlines[0]
#     long_hlines.index.name='x0'
#     long_hlines = long_hlines.reset_index()
#
#     return long_hlines.rename(columns={0:'y0'})

#####################################################################################


def plot_df(self):
    fig = go.Figure(data=[go.Candlestick(x=self.df.index, open=self.df['open'], high=self.df['high'], low=self.df['low'], close=self.df['close'])], layout=go.Layout())
    fig.update_layout(title=self.name, xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price', template="plotly_dark")
    fig.update_traces(increasing_line_color= 'white', selector = dict(type='candlestick'))
    fig.update_traces(decreasing_line_color= 'orange', selector = dict(type='candlestick'))

    # for row in self.long_hlines.index:
    #     x0, y0, x1, y1 = self.long_hlines.loc[row].values
    #     fig.add_shape(type='line', line=dict(color='red'), label=dict(text=y1, textposition='end', padding=0, font=dict(size=10),xanchor='right', yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

    return fig


def test_holds(holds:pd.Series, tests:pd.Series, func:bool, hold=None, longs=None, total=None) -> pd.DataFrame:
  #  Test hold levels based on mask usually series.isin(test

    mask = func

    ix_drop = holds[mask].index
    dropped = f'Drop: {len(ix_drop)} '

    untested = holds.drop(labels=ix_drop)
    print(f'Total Holds:{total}  Dropped:{dropped}  Untested:{len(untested)}\n')

    return untested


