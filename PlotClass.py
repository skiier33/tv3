
import plotly.graph_objects as go
import pandas as pd
from DataClass import HoldCandle, Untested
import matplotlib.pyplot as plt
from functools import wraps


###################################################################################################################################################
###################################################################################################################################################

class PlotCandle(HoldCandle):

    def __init__(self, holdcandle, testcandle):
        self.hc=holdcandle
        self.tc = testcandle
        self.df = self.hc.df
        self.name = self.hc.name

        self.long_hlines = self.get_hlines(self.tc.longs)
        self.short_hlines = self.get_hlines(self.tc.shorts)
        self.fig = self.plot()
        self.fig.show()
        self.lfig = self.add_lines(self.long_hlines, self.fig, color='green')
        self.lfig.show()
        self.sfig = self.add_lines(self.short_hlines, self.fig, color='red')
        self.sfig.show()

        # self.fig_holds = self.plot2()

    def get_hlines(self, hold)->pd.DataFrame:
        hlines = pd.DataFrame(hold)
        hlines['x1'] = self.df.index[-1]
        hlines['y1'] = hlines[0]
        hlines.index.name='x0'
        hlines = hlines.reset_index()
        return hlines.rename(columns={0:'y0'})


    def plot(self, **kwargs):
        fig = go.Figure(data=[go.Candlestick(x=self.df.index, open=self.df['open'], high=self.df['high'], low=self.df['low'], close=self.df['close'])], layout=go.Layout())
        fig.update_layout(title=self.name, xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price', template="plotly_dark")
        fig.update_traces(increasing_line_color='white', selector=dict(type='candlestick'))
        fig.update_traces(decreasing_line_color='blue', selector=dict(type='candlestick'))
        return fig

    def add_lines(self, hlines, fig, color):


        for row in hlines.index:
            x0, y0, x1, y1 = hlines.loc[row].values
            fig.add_shape(type='line', line=dict(color=color), label=dict(text=y1, textposition='end', padding=0, font=dict(size=10), xanchor='right', yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)
        return fig

 ###################################################################################################################################################
###################################################################################################################################################


class Plot2(PlotCandle):
    def __init__(self, holdcandle, testcandle, plot_kws=[], **kwargs):
        super().__init__(holdcandle, testcandle)
        self.plot_kws = plot_kws

        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])
            self.plot_kws.append(k)

        self.fig = self.plot()

    def plot_longs(self):
        self.add_lines(self.long_hlines, self.fig, color='green')

    def plot_shorts(self):
        self.add_lines(self.short_hlines, self.fig, color='red')

    def plot_both(self):
        self.plot_longs()
        self.plot_shorts()

    def modplot(self):
        for kw in self.plot_kws:
            print(kw, self.__dict__[kw])
            self.fig.layout[kw] = self.__dict__[kw]


    ###################################################################################################################################################
    ###################################################################################################################################################
