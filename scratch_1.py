INTERVALS = ['in_1_minute', 'in_3_minute', 'in_5_minute', 'in_15_minute', 'in_1_hour', 'in_4_hour', 'in_daily']
COLORS = ['grey', 'pink', 'green', 'orange', 'blue', 'yellow', 'red']
N_BARS = [5000, 1666, 1000, 333, 83, 21, 3]
colors_dict = dict(zip(INTERVALS, COLORS))
n_dict = dict(zip(INTERVALS, N_BARS))




import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from DataClass import  TestCandle, HoldCandle , Untested, UT2, TimeFrame, ThreeDay
import plotly.graph_objects as go
import plotly.io as pio
pio.templates

username = 'Fook_Yew'
password = 'Tr4d1ng1sc00l'
tv = TvDatafeed(username, password)
interval = INTERVALS[5]
n_bars=n_dict[interval]


testcandle = TestCandle(Interval.in_1_minute, n_bars=100)
holdcandle = HoldCandle(Interval[interval], n_bars)

timeframe = TimeFrame(holdcandle, testcandle)



print('fdg')
