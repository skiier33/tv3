
import numpy as np
import plotly.io as pio
from tvDatafeed import Interval , TvDatafeed
import plotly.graph_objects as go
import pandas as pd

pio.templates

username = 'Fook_Yew'
password = 'Tr4d1ng1sc00l'
tv = TvDatafeed(username, password)


 ##########################################

class TestCandle:

    def __init__(self, interval: Interval, n_bars: int) -> object:

        self.interval = interval
        self.n_bars:int = n_bars
        self.name = self.set_name()
        self.df = self.set_df()
        self.long_tester = self.get_long_tester()
        self.short_tester = self.get_short_tester()


    def set_name(self) -> str:
        return str(self.interval).split('.in_')[-1]

    def set_df(self) -> pd.DataFrame:
        return tv.get_hist(symbol='BTCUSDT.P', exchange='zoomex', interval=self.interval, n_bars=self.n_bars)

    def get_long_tester(self) -> pd.DataFrame:
        return self.df.low

    def get_short_tester(self)->pd.DataFrame:
        return self.df.high

############################################################################################################################################

class HoldCandle:

    def __init__(self, interval, n_bars):

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

############################################################################################################################################


class Untested(HoldCandle, TestCandle):
    """
    will allow to get any properties from parent hold or test but must pass as args
    """
    def __init__(self, holdcandle, testcandle) -> object:

        self.holdcandle =holdcandle
        self.testcandle =testcandle
        self.name = self.holdcandle.name
        self.name_test=self.testcandle.name

        self.set_longs()
        self.set_shorts()

    def test_hold(self, hold, test) -> pd.DataFrame:
        """
        Tests hold levels with another time frame
        :return:Untested hold levels for test time
        """
        self.hold = hold
        self.test = test

        print(f' To Test: {len(self.hold)}')

        #return true where tester is in
        mask = self.hold.isin(self.test)
        ix_drop = self.hold[mask].index

        return self.hold.drop(labels=ix_drop)

    def set_longs(self):
        self.longs = self.test_hold(self.holdcandle.longs, self.testcandle.long_tester)

    def set_shorts(self):
        self.shorts = self.test_hold(self.holdcandle.shorts, self.testcandle.short_tester)

############################################################################################################################################
