from DataClass import  TestCandle, HoldCandle, BasePlot
from tvDatafeed import Interval
import plotly.graph_objects as go
import pandas as pd
import copy

from tvdataclass.DataClass import HoldCandle, TestCandle, BasePlot

holdcandle = BasePlot(Interval.in_15_minute, 50)

# holdcandle.plot_df()

testcandle = TestCandle(Interval.in_1_minute, 1000)


class Untested(BasePlot, TestCandle):

    def __init__(self, holdcandle, testcandle):
        self.holdcandle = holdcandle
        self.testcandle = testcandle
    

    def test_hold(self) ->pd.DataFrame:
        """
        Tests hold levels with another time frame
        :return:Untested hold levels for test time
        """

        print(f'To Test: {len(self.holdcandle.longs)}')

        ix = ~holdcandle.longs.isin(testcandle.long_tester)

        ix = ix.loc[ix]
        print(f'Untested: {len(ix)}')

        return self.holdcandle.longs[ix.index]




ix = test_hold(holdcandle, testcandle)


print('sdfsdfsd')

pd.Series.item
