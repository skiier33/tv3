import plotly.graph_objects as go
import pandas as pd
from DataClass import Candle

import plotly.graph_objects as go
import pandas as pd




class BasePlot(Candle):

    def __init__(self, interval, n_bars):
        self.interval=interval
        self.n_bars=n_bars
    #     self.plot_df()
    #
    # def plot_df(self):
    #
    #     fig = go.Figure(data=[go.Candlestick(x=self.df.index,
    #                     open=self.df['Open'], high=self.df['High'],
    #                     low=self.df['Low'], close=self.df['Close'])])
    #
    #     fig.update_layout(title=self.name, xaxis_title='Date', yaxis_title='Price')
    #
    #
    #     fig.show()
