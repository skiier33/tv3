
import numpy as np
from tvDatafeed import TvDatafeed
import plotly.io as pio


from tvDatafeed import Interval
import plotly.graph_objects as go
import pandas as pd

from DataClass import HoldCandle, Untested, TestCandle, BasePlot
from PlotClass import UntestedPlot

pio.templates

username = 'Fook_Yew'
password = 'Tr4d1ng1sc00l'
tv = TvDatafeed(username, password)


testcandle = TestCandle(Interval.in_1_minute,500)


class Daily:
    def __init__(self, nbars=3, testcandle=testcandle):

        self.nbars = nbars
        self.color = 'red'
        self.testcandle = testcandle
        self.interval = Interval.in_daily
        self.holdcandle = HoldCandle(self.interval, self.nbars)
        self.untapped = Untested(self.holdcandle, self.testcandle)

        self.kwargs = self.untapped.__dict__
        self.untappedplot = UntestedPlot(self.holdcandle.df, **self.kwargs)
        # self.plot = UntestedPlot(self.holdcandle.df, **self.kwargs)

        def add_plot_class(self):
            self.base_plot = BasePlot(self.holdcandle.df, **self.kwargs)





d = Daily()


print('aasdas')































































#
#
# class FourHr:
#     def __init__(self, nbars=21, testcandle=testcandle):
#
#         self.nbars = nbars
#         self.color = 'red'
#         self.testcandle = testcandle
#         self.interval = Interval.in_4_hour
#         self.holdcandle = HoldCandle(self.interval, self.nbars)
#         self.untapped = Untested(self.holdcandle, self.testcandle)
#
#         self.kwargs = self.untapped.__dict__
#         self.untappedplot = UntestedPlot(self.holdcandle.df, **self.kwargs)
#
#
# class OneHr:
#     def __init__(self, nbars=83, testcandle=testcandle):
#
#         self.nbars = nbars
#         self.color = 'blue'
#         self.testcandle = testcandle
#         self.interval = Interval.in_1_hour
#         self.holdcandle = HoldCandle(self.interval, self.nbars)
#         self.untapped = Untested(self.holdcandle, self.testcandle)
#
#         self.kwargs = self.untapped.__dict__
#         self.untappedplot = UntestedPlot(self.holdcandle.df, **self.kwargs)
#
#
# class FtnMin:
#     def __init__(self, nbars=83, testcandle=testcandle):
#
#         self.nbars = nbars
#         self.color = 'blue'
#         self.testcandle = testcandle
#         self.interval = Interval.in_15_minute
#         self.holdcandle = HoldCandle(self.interval, self.nbars)
#         self.untapped = Untested(self.holdcandle, self.testcandle)
#
#         self.kwargs = self.untapped.__dict__
#         self.untappedplot = UntestedPlot(self.holdcandle.df, **self.kwargs)
#
#
# class FiveMin:
#     def __init__(self, nbars=1000, testcandle=testcandle):
#         self.nbars = nbars
#         self.color = 'green'
#         self.testcandle = testcandle
#         self.interval = Interval.in_5_minute
#         self.holdcandle = HoldCandle(self.interval, self.nbars)
#         self.untapped = Untested(self.holdcandle, self.testcandle)
#
#         self.kwargs = self.untapped.__dict__
#         self.untappedplot = UntestedPlot(self.holdcandle.df, **self.kwargs)
#
#
# class ThreeMin:
#     def __init__(self, nbars=1667, testcandle=testcandle):
#         self.nbars = nbars
#         self.color = 'pink'
#         self.testcandle = testcandle
#         self.interval = Interval.in_3_minute
#         self.holdcandle = HoldCandle(self.interval, self.nbars)
#         self.untapped = Untested(self.holdcandle, self.testcandle)
#
#         self.kwargs = self.untapped.__dict__
#         self.untappedplot = UntestedPlot(self.holdcandle.df, **self.kwargs)
#
#
# class OneMin:
#     def __init__(self, nbars=5000, testcandle=testcandle):
#         self.nbars = nbars
#         self.color = 'grey'
#         self.testcandle = testcandle
#         self.interval = Interval.in_1_minute
#         self.holdcandle = HoldCandle(self.interval, self.nbars)
#         self.untapped = Untested(self.holdcandle, self.testcandle)
#
#         self.kwargs = self.untapped.__dict__
#         self.untappedplot = UntestedPlot(self.holdcandle.df, **self.kwargs)
