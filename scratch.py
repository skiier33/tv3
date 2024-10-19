import pandas as pd
from CONSTANTS import df as df
from tvDatafeed import TvDatafeed,  Interval

from DataClass import *
from PlotClass import *

tc = TestCandle(interval=Interval.in_1_minute,  n_bars=100)

for i in df.index[1:]:
    ix = Interval[i]
    n =int( df['n'].loc[i])
    hc = HoldCandle(interval=Interval[i], n_bars=n)
    print(f'testing {i}')
    ut = Untested(hc, tc)
    p = PlotCandle(hc, ut)



print('rweferfre')








print('jonuiio')
