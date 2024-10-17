from DataClass import  TestCandle, HoldCandle , Untested
from PlotClass import BasePlot , UntestedPlot
from tvDatafeed import Interval
import plotly.graph_objects as go
import pandas as pd
import copy


testcandle = TestCandle(Interval.in_4_hour, n_bars=300)

holdcandle = BasePlot(Interval.in_daily, 50)





ut = Untested(holdcandle, testcandle)





print('sdfsdfsd')

pd.Series.item
