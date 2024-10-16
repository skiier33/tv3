import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tvDatafeed import TvDatafeed, Interval
import pickle
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
pio.templates

username = 'Fook_Yew'
password = 'Tr4d1ng1sc00l'
tv = TvDatafeed(username, password)

intervals = ['in_1_minute', 'in_3_minute', 'in_5_minute', 'in_15_minute', 'in_1_hour', 'in_4_hour', 'in_daily',
             'in_weekly']
colors = ['grey', 'pink', 'green', 'orange', 'blue', 'yellow', 'red', 'purple']
mins = [1, 3, 5, 15, 60, 240, 1440, 43200]
colors_dict = dict(zip(intervals, colors))
n_dict = dict(zip(intervals, mins))


class Candle:

    def __init__(self, interval, n_bars):
        """

        :param interval:
        :type interval:
        :param n_bars:
        :type n_bars:
        """

        self.interval = interval
        self.n_bars:int = n_bars
        self.name = self.set_name()

        self.df = self.set_df()
        self.get_hold_indexs()
        self.longs = self.get_longs()
        self.shorts= self.get_shorts()

    def set_name(self)->str:

        return str(self.interval).split('.in_')[-1]

    def __repr__(self):

        return (f' Timeframe: {self.name} \n Candles: {str(self.n_bars)} \n Start: {self.df.index[0]} \n '
                f'End: {self.df.index[-1]} \n Shorts: {len(self.shorts) / 2}   Longs: {len(self.longs) / 2} ')




    def set_df(self)->pd.DataFrame:

        return tv.get_hist(symbol='BTCUSDT.P', exchange='zoomex', interval=self.interval, n_bars=self.n_bars)


    def get_hold_indexs(self)->None:

        self.short_indexes = []
        self.long_indexes = []

        self.df['up_down'] = np.sign(self.df.close - self.df.open)

        for time in self.df.index[:-4]:

            sl = slice(time, time + 3 * (self.df.index[1] - self.df.index[0]))
            chunk = self.df.loc[sl]

            if all(chunk['up_down'] == [1, 1, -1, -1]):

                self.short_indexes.extend(chunk.index[:2])

            elif all(chunk['up_down'] == [-1, -1, 1, 1]):

                self.long_indexes.extend(chunk.index[:2])

    def get_longs(self)->pd.DataFrame:

        return pd.concat([ self.df.loc[self.long_indexes].high,  self.df.loc[self.long_indexes].open]).sort_index()

    def get_shorts(self)->pd.DataFrame:

        return pd.concat([self.df.loc[self.short_indexes].low, self.df.loc[self.short_indexes].open]).sort_index()


class BasePlot(Candle):

    def __init__(self, interval, n_bars):
        super().__init__(interval, n_bars)
        self.long_hlines = self.get_hlines()
        self.fig = self.plot_df()


    def get_hlines(self)->pd.DataFrame:

        long_hlines = pd.DataFrame(self.longs)
        long_hlines['x1'] = self.df.index[-1]
        long_hlines['y1'] = long_hlines[0]
        long_hlines.index.name='x0'
        long_hlines = long_hlines.reset_index()


        return long_hlines.rename(columns={0:'y0'})



    def plot_df(self):

        fig = go.Figure(data=[go.Candlestick(x=self.df.index,
                        open=self.df['open'], high=self.df['high'],
                        low=self.df['low'], close=self.df['close'])], layout=go.Layout())

        fig.update_layout(title=self.name, xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price', template="plotly_dark")

        # fig.update_traces(name='fff',  selector = dict(type='candlestick'))

        fig.update_traces(increasing_line_color= 'white', selector = dict(type='candlestick'))

        fig.update_traces(decreasing_line_color= 'blue', selector = dict(type='candlestick'))

        for row in self.long_hlines.index:
           x0, y0, x1, y1 = self.long_hlines.loc[row].values
           fig.add_shape(type='line', line=dict(color='red'), label=dict(text=y1, textposition='end', padding=0, font=dict(size=10), xanchor='right', yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

        return fig


class HoldCandle:

    def __init__(self, interval, n_bars):
        """

        :param interval:
        :type interval:
        :param n_bars:
        :type n_bars:
        """

        self.interval = interval
        self.n_bars:int = n_bars
        self.name = self.set_name()

        self.df = self.set_df()
        self.get_hold_indexs()
        self.longs = self.get_longs()
        self.shorts= self.get_shorts()

    def set_name(self)->str:

        return str(self.interval).split('.in_')[-1]

    def __repr__(self):

        return (f' Timeframe: {self.name} \n Candles: {str(self.n_bars)} \n Start: {self.df.index[0]} \n '
                f'End: {self.df.index[-1]} \n Shorts: {len(self.shorts) / 2}   Longs: {len(self.longs) / 2} ')

    def set_df(self)->pd.DataFrame:

        return tv.get_hist(symbol='BTCUSDT.P', exchange='zoomex', interval=self.interval, n_bars=self.n_bars)

    def get_hold_indexs(self)->None:

        self.short_indexes = []
        self.long_indexes = []

        self.df['up_down'] = np.sign(self.df.close - self.df.open)

        for time in self.df.index[:-4]:

            sl = slice(time, time + 3 * (self.df.index[1] - self.df.index[0]))
            chunk = self.df.loc[sl]

            if all(chunk['up_down'] == [1, 1, -1, -1]):

                self.short_indexes.extend(chunk.index[:2])

            elif all(chunk['up_down'] == [-1, -1, 1, 1]):

                self.long_indexes.extend(chunk.index[:2])

    def get_longs(self)->pd.DataFrame:

        return pd.concat([ self.df.loc[self.long_indexes].high,  self.df.loc[self.long_indexes].open]).sort_index()

    def get_shorts(self)->pd.DataFrame:

        return pd.concat([self.df.loc[self.short_indexes].low, self.df.loc[self.short_indexes].open]).sort_index()


class TestCandle(Candle):

    def __init__(self, interval: Interval, n_bars: int) -> object:
        """

        :param interval:
        :type interval:
        :param n_bars:
        :type n_bars:
        """

        self.interval = interval
        self.n_bars:int = n_bars
        self.name = self.set_name()
        self.df = self.set_df()
        self.long_tester = self.get_long_tester()
        self.short_tester = self.get_short_tester()

    def get_long_tester(self) -> pd.DataFrame:

        return  self.df.low

    def get_short_tests(self)->pd.DataFrame:

        return self.df.high

    def set_name(self)->str:

        return str(self.interval).split('.in_')[-1]

    def set_df(self)->pd.DataFrame:

        return tv.get_hist(symbol='BTCUSDT.P', exchange='zoomex', interval=self.interval, n_bars=self.n_bars)

 fn testcan( )
    def


class Untapped(HoldCandle, TestCandle):
    def __init__(self, holdcandle, testcandle):










# class oldTester:
#
#
#     def __init__(self, hold_interval, hold_nbars, test_interval, test_nbars):
#         '''
#
#         :param hold_interval:hold interval
#         :type hold_interval:
#         :param hold_nbars:hold number of cabdled
#         :type hold_nbars:
#         :param test_interval:
#         :type test_interval:
#         :param test_nbars:
#         :type test_nbars:
#         '''
#         self.hold_interval = hold_interval
#         self.hold_nbars = hold_nbars
#         self.test_interval = test_interval
#         self.test_nbars = test_nbars
#
#         self.hold_candle = Candle(self.hold_interval, self.hold_nbars)
#         self.test_candle = Candle(self.test_interval, self.test_nbars)
#
#
#         self.long_holds = self.set_hold_df(self.long_holds)
#
#         self.short_holds = self.set_hold_df(self.short_holds)
#
#         self.untapped_longs = self.test_long_holds()
#         self.untapped_longs.copy()
#         self.untapped_shorts = self.test_short_holds()
#
#
#
#
#
#     def test_long_holds(self):
#         '''
#
#         :param self:
#         :return: untapped longs
#         '''
#         self.ix_tapped = None
#
#         print(f'Starting Long testings \n\n Long Holds: {len(self.long_holds)} before testing')
#
#         low_tester = self.test_candle.df['low'].values
#
#         mask = ~ self.long_holds.isin(low_tester)
#
#         self.ix_tapped = self.long_holds[mask].dropna().index
#
#         self.longs_untapped = self.long_holds.drop(self.ix_tapped)
#
#         print(f'Longs tested, {len(self.ix_tapped)} \n Untested: {self.longs_untapped} \n\n\n\n\n')
#
#         return self.longs_untapped
#
#     def test_short_holds(self):
#         '''
#
#         :param self:
#         :return:untapped shorts
#         '''
#         self.ix_tapped = None
#         print(f' Short Holds: {len(self.short_holds)} before testing')
#
#         tester = self.test_candle.df['high'].values
#
#         mask = ~ self.short_holds.isin(tester)
#
#         self.ix_tapped = self.short_holds[mask].dropna().index
#
#         self.shorts_untapped = self.short_holds.drop(self.ix_tapped)
#
#
#
#         return self.shorts_untapped
#
#
# class Untapped(Tester):
#
#      def __init__(self, hold_interval, hold_nbars, test_interval, test_nbars):
#          super().__init__(hold_interval=hold_interval, hold_nbars=hold_nbars, test_interval=test_interval, test_nbars=test_nbars)
