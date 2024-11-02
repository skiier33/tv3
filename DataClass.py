import datetime

from CONSTANTS import  CSVS
import pathlib
import pandas as pd
import numpy as np
from data_funcs import read_binance_csv, plot_df
import re
import plotly.graph_objects as go




class FolderData:
    """Create an object of dataframes for all csvs in a folder

    """
    def __init__(self, csv_folder: str,*args, **kwargs) -> None:
        self.csv_folder = pathlib.Path(csv_folder)
        self.files = list(self.csv_folder.glob('*.csv'))

        for file in self.files:
            self.name = file.parts[-1].split('.')[0]
            self.df = TimeFrameData(read_binance_csv(file))

            self.__setattr__(f'__{self.name}', self.df)


class TimeFrameData:
    def __init__(self,df:pd.DataFrame) -> None:
        self.df = df
        self.dt = df.index[1] - df.index[0]
        self.name = str(self.dt)
        self.n_bars = int(len(df))
        self.df['up_down'] = np.sign(self.df.close - self.df.open)
        self.df.sort_index(inplace=True)
        self.start = self.df.index[0]
        self.end = self.df.index[-1]

        self.long_indexs = []
        self.short_indexs = []
        self.longs = None
        self.shorts = None

        print(f'Loaded {self.name} Timeframe Data \n'
              f'Start: {self.start}\n'
              f' End: {self.end} \n'
              f' {self.n_bars} bars')


    def round_df(self):
       # self.df =  self.df.round(digits)
       return self.df.round(self.round_digits)

        # self.get_untested()

    def get_untested(self):
        for time in self.df.index[:-4]:

            try:
                t2 = self.df.index.get_loc(time)+3
            except(TypeError):
                print(f'type error at {time}')
                t2a = time + 3*self.dt
                continue
            sl = slice(time, self.df.index[t2])
            chunk = self.df.loc[sl]
            try:
                if all(chunk['up_down'] ==  [1, 1, -1, -1]):
                    self.short_indexs.extend(chunk.index[:2])
                elif all(chunk['up_down'] ==  [-1,-1, 1, 1]):
                    self.long_indexs.extend(chunk.index[:2])

            except(ValueError):
                print(f'Valeue error at {time}')

                continue


        self.longs = pd.concat([self.df['open'].loc[self.long_indexs], self.df['high'].loc[self.long_indexs]]).sort_index()
        self.shorts = pd.concat([self.df['open'].loc[self.short_indexs], self.df['low'].loc[self.short_indexs]]).sort_index()

        print(f'Total Longs: {len(self.longs)} \n'
              f'Total  Shorts: {len(self.shorts)}')

class TimeFramePlot:
    """
    TimeFramePlot
    =============
    A class for creating, modifying, and visualizing candlestick plots with additional horizontal lines for long and short entries using Plotly and pandas.

    Methods
    -------
    __init__:
        Initializes the TimeFramePlot with a pandas DataFrame, generates the base candlestick plot, and adds horizontal lines.

    plot_df:
        Generates a plotly candlestick figure from the DataFrame.

    get_hlines:
        Converts long or short entry data from the DataFrame into a format suitable for adding as horizontal lines to the plot.

    add_long_lines:
        Adds horizontal lines representing long entries to the plot.

    add_short_lines:
        Adds horizontal lines representing short entries to the plot.
    """
    def __init__(self,timeframedata:pd.DataFrame) -> pd.DataFrame:
        """
        :param timeframedata: A pandas DataFrame containing time series data required for plotting and analysis.
        """
        self.timeframedata = timeframedata
        self.fig = self.plot_df()
        self.long_hlines = self.get_hlines('longs')
        self.short_hlines = self.get_hlines('shorts')
        self.longfig = self.add_long_lines()
        self.shortfig = self.add_short_lines()
        # self.longfig = self.add_long_lines(self.long_hlines)


    def plot_df(self):
        """
        Generates and returns a candlestick plot of the dataframe stored in the timeframedata attribute. The plot is styled with a dark theme, includes custom colors for the candlestick traces, and hides the x-axis range slider.

        :return: A Plotly Figure object containing the candlestick plot
        """
        fig = go.Figure(
            data=[go.Candlestick(x=self.timeframedata.df.index, open=self.timeframedata.df['open'], high=self.timeframedata.df['high'], low=self.timeframedata.df['low'], close=self.timeframedata.df['close'])],
            layout=go.Layout())
        fig.update_layout(title=self.timeframedata.name, xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price',
                          template="plotly_dark")
        fig.update_traces(increasing_line_color='white', selector=dict(type='candlestick'))
        fig.update_traces(decreasing_line_color='cyan', selector=dict(type='candlestick'))

        return fig

    def get_hlines(self, long_short) -> pd.DataFrame:
        """
        :param long_short: A string key to access a specific dataframe from `self.timeframedata`.
        :return: A pandas DataFrame with renamed columns 'x0', 'y0', 'x1', and 'y1'.
        """
        hlines = pd.DataFrame(self.timeframedata.__dict__[long_short])
        hlines['x1'] = hlines.index[-1]
        hlines['y1'] = hlines[0]
        hlines.index.name = 'x0'
        hlines = hlines.reset_index()

        return hlines.rename(columns={0: 'y0'})


    def add_long_lines(self) -> go.Figure:
        """
        Adds long horizontal lines to the figure stored in the instance.

        :return: A Plotly Figure object with added long horizontal lines.
        """
        # fig = fig

        for row in self.long_hlines.index:
            x0, y0, x1, y1 = self.long_hlines.loc[row].values
            self.fig.add_shape(type='line', line=dict(color='green'),
                               label=dict(text=y1, textposition='end', padding=0, font=dict(size=10), xanchor='right',
                                          yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

        return self.fig


    def add_short_lines(self) -> go.Figure:
        # fig = fig

        for row in self.short_hlines.index:
            x0, y0, x1, y1 = self.short_hlines.loc[row].values
            self.fig.add_shape(type='line', line=dict(color='red'),
                               label=dict(text=y1, textposition='end', padding=0, font=dict(size=10),
                                          xanchor='right',
                                          yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

        return self.fig
        #






