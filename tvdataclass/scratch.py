from DataClass import  TestCandle, HoldCandle , Untested, UT2
from PlotClass import BasePlot , UntestedPlot
from tvDatafeed import Interval
import plotly.graph_objects as go
import pandas as pd
import copy

def plot_holds(ih,   nh, it, nt):


    holdcandle = BasePlot(ih, n_bars=nh)
    testcandle = TestCandle(it, n_bars=nt)

    df = holdcandle.df

    fig = holdcandle.plot()
    fig.show()

    ut = Untested(holdcandle, testcandle)

    k = ut.__dict__

    df = k['holdcandle'].df

    utp = UntestedPlot(df, **k)
    fig2 =  utp.plot()
    fig2.show()

    return k


k = plot_holds(Interval.in_4_hour, 300, Interval.in_1_hour, 1200)


print('dfghdf')
