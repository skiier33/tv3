from DataClass import  TestCandle, HoldCandle , Untested
from PlotClass import UntestedPlot
from tvDatafeed import Interval

from DataClass import intervals

INTERVALS = ['in_1_minute', 'in_3_minute', 'in_5_minute', 'in_15_minute', 'in_1_hour', 'in_4_hour', 'in_daily']
COLORS = ['grey', 'pink', 'green', 'orange', 'blue', 'yellow', 'red']
N_BARS = [5000, 1666, 1000, 333, 83, 21, 3]

INTERVALS = ['in_1_minute', 'in_3_minute', 'in_5_minute', 'in_15_minute', 'in_1_hour', 'in_4_hour', 'in_daily']
COLORS = ['grey', 'pink', 'green', 'orange', 'blue', 'yellow', 'red']
N_BARS = [5000, 1666, 1000, 333, 83, 21, 3]
colors_dict = dict(zip(INTERVALS, COLORS))
n_dict = dict(zip(INTERVALS, N_BARS))
TC = TestCandle(Interval.in_1_minute, n_bars=5000)

interval = intervals[5]

n_bars=n_dict[interval]

color = colors_dict[interval]



holdcandle = HoldCandle(Interval[interval], n_bars)

class TimeFrame(HoldCandle):
    def __init__(self, holdcandle, color):

        self.candle = holdcandle
        self.color = color
        self.untapped = None
        self.dict = None
        self.df = None
        self.utp = None
        self.fig = None


        def set_untested(self):

            self.untapped = Untested(self.candle, TC)

            self.dict = self.untested.__dict__
            self.df = self.dict['holdcandle'].df
            self.utp = UntestedPlot(self.df, **self.dict)
            self.fig = self.utp.plot()
            self.fig.show()



class ThreeDay:
    def __init__(self, interval, n_bars, color):



        self.untested = None
        self.dict =None
        self.df =None
        self.utp =None
        self.fig = None

        self.set_untested()


        def set_untested(self):

            self.untested = Untested(self.candle, TC)
            self.dict = self.untested.__dict__
            self.df = self.dict['holdcandle'].df
            self.utp = UntestedPlot(self.df, **self.dict)
            self.fig = self.utp.plot()
            self.fig.show()


# print('dsffd')
#
# for i in INTERVALS:
#     print(i)
#
#     tf = ThreeDay(i, n_dict[i], n_dict[i], colors_dict[i])

# @classmethod
    # def get_testcandle(interval=Interval.in_1_minute, nbars=5000):

print('dfghdf')
