from pickletools import long1

import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
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




class HoldCandle:
    #
    # @classmethod
    # def __getattr__(self, attr:str=None):
    #     """
    #     Get any attribute value
    #     :param attr:Names of attribute (att of attribute)
    #     :return: self.att
    #     """
    #
    #     return getattr(self, attr)

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

    def __init__(self, holdcandle, testcandle):
        """
        :param holdcandle:HoldCandle
        :param testcandle:TestCandle
        """
        self.holdcandle = holdcandle
        self.testcandle = testcandle
        self.longs = self.test_hold(self.holdcandle.longs, self.testcandle.long_tester)
        self.shorts = self.test_hold(self.holdcandle.shorts, self.testcandle.short_tester)

    def test_hold(self, hold, test) -> pd.DataFrame:
        """
        Tests hold levels with another time frame
        :return:Untested hold levels for test time
        """
        self.hold = hold
        self.test = test

        print(f'To Test: {len(self.hold)}')

        ix = ~self.hold.isin(self.test)

        ix = ix.loc[ix]
        print(f'Untested: {len(ix)}')

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
