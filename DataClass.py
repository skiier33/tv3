
import numpy as np
from tvDatafeed import TvDatafeed
import plotly.io as pio


from tvDatafeed import Interval
import plotly.graph_objects as go
import pandas as pd


pio.templates

username = 'Fook_Yew'
password = 'Tr4d1ng1sc00l'
tv = TvDatafeed(username, password)

INTERVALS = ['in_1_minute', 'in_3_minute', 'in_5_minute', 'in_15_minute', 'in_1_hour', 'in_4_hour', 'in_daily']
COLORS = ['grey', 'pink', 'green', 'orange', 'blue', 'yellow', 'red']
N_BARS = [5000, 1666, 1000, 333, 83, 21, 3]
colors_dict = dict(zip(INTERVALS, COLORS))
n_dict = dict(zip(INTERVALS, N_BARS))



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


class BasePlot(HoldCandle):

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


class TestCandle:

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
        self.long_tester.name = 'longs'
        self.short_tester = self.get_short_tester()
        self.short_tester.name = 'shorts'

    def set_name(self) -> str:
        return str(self.interval).split('.in_')[-1]

    def set_df(self) -> pd.DataFrame:
        return tv.get_hist(symbol='BTCUSDT.P', exchange='zoomex', interval=self.interval, n_bars=self.n_bars)

    def get_long_tester(self) -> pd.DataFrame:

        return  self.df.low

    def get_short_tester(self)->pd.DataFrame:

        return self.df.high

    def set_name(self)->str:

        return str(self.interval).split('.in_')[-1]

    def set_df(self)->pd.DataFrame:

        return tv.get_hist(symbol='BTCUSDT.P', exchange='zoomex', interval=self.interval, n_bars=self.n_bars)


class Untested(HoldCandle, TestCandle):
    """
    will allow to get any properties from parent hold or test but must pass as args
    """

    def __init__(self, holdcandle, testcandle, *args, **kwargs) -> object:
        """
        :param holdcandle:HoldCandle
        :param testcandle:TestCandle
        :returns self.holdcandle = holdcandle
                 self.testcandle = testcandle
                 self.name_test
                self.untested lonfs
                 self.untested shorts
        """
        self.holdcandle =holdcandle
        self.testcandle =testcandle
        self.name_test=self.testcandle.set_name()
        self.args = args
        self.kwargs = kwargs

        self.set_longs()
        self.set_shorts()

    def get_test_name(self):

        self.name_test =  self.testcandle.name

    def set_longs(self):

        self.untested_longs = self.test_hold(self.holdcandle.longs, self.testcandle.long_tester)

    def set_shorts(self):

        self.untested_shorts = self.test_hold(self.holdcandle.shorts, self.testcandle.short_tester)

    def test_hold(self, hold, test) -> pd.DataFrame:
        """
        Tests hold levels with another time frame
        :return:Untested hold levels for test time
        """
        self.hold = hold
        self.test = test

        print(f' To Test: {len(self.hold)}')

        #check is test is not in hold
        ix = ~self.hold.isin(self.test)


        ix = ix.loc[ix]
        print(f'Untested: {len(ix)} \n\n')

        return self.hold.loc[ix]


class UT2(Untested):

    def __init__(self,**kwargs):
        self.kwargs = kwargs




class TimeFrame(HoldCandle, TestCandle):



    def __init__(self, holdcandle, testcandle, *args, **kwargs) -> object:

        self.candle = holdcandle
        self.testcandle = testcandle
        self.untapped =None
        self.dict = None
        self.df = None
        self.utp = None
        self.fig = None
