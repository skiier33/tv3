import pandas as pd
from TEST_CONSTANTS import df as df
from tvDatafeed import TvDatafeed,  Interval

from DataClass import *
from PlotClass import *

tc = TestCandle(interval=Interval.in_1_minute,  n_bars=100)

for i in df.index[1:3]:
    ix = Interval[i]
    n =int( df['n'].loc[i])
    hc = BasePlot(interval=Interval[i], n_bars=n)
    ut = Untested(hc, tc)
    fig = hc.fig
    fig.show()
