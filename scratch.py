import pandas as pd
from CONSTANTS import df as df
from tvDatafeed import TvDatafeed,  Interval

from DataClass import *



for i in df.index[:3]:
    ix = Interval[i]
    n =int( df['n'].loc[i])
    hc = HoldCandle(interval=Interval[i], n_bars=n)
    hc.df.columns
