"""Classes used to mae plots"""
import plotly.graph_objects as go
import pandas as pd

from DataClass import HoldCandle


class PlotCandle(HoldCandle):
    """
    """
    def __init__(self, untested, hold_df, test_df, **kwargs):

        super().__init__(hold_df, test_df, **kwargs)
        self.long_hlines = self.get_hlines(self.hc.longs)
        self.short_hlines = self.get_hlines(self.hc.shorts)

    def get_hlines(self, hold) -> pd.DataFrame:
        """
        """
        hlines = pd.DataFrame(hold)
        hlines['x1'] = self.df.index[-1]
        hlines['y1'] = hlines[0]
        hlines.index.name = 'x0'
        hlines = hlines.reset_index()

        return hlines.rename(columns={0: 'y0'})

    def plot(self, update_layout=None, **kwargs):
        """
        """
        fig = go.Figure(data=[ go.Candlestick(x=self.df.index, open=self.df['open'], high=self.df['high'], low=self.df['low'], close=self.df['close'])], layout=go.Layout())
        fig.update_layout(title=self.name, xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price', template="plotly_dark")
        fig.update_layout(autosize=True, width=1600, height=600)
        fig.update_traces(increasing_line_color='white', selector=dict(type='candlestick'))
        fig.update_traces(decreasing_line_color='blue', selector=dict(type='candlestick'))

        return fig

    @staticmethod
    def add_lines(hlines, fig, color=None):
        """
        """
        for row in hlines.index:
            x0, y0, x1, y1 = hlines.loc[row].values
            fig.add_shape(type='line', line=dict(color=color),
                          label=dict(text=y1, textposition='end', padding=0, font=dict(size=10), xanchor='right',
                                     yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

        return fig


class Plot2(PlotCandle):
    """
    """
    def __init__(self, ut, plot_kws=[None], **kwargs):
        super().__init__(ut)
        self.plot_kws = plot_kws

        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])
            self.plot_kws.append(k)

        self.fig = self.plot()

    def plot_longs(self):
        """
        """
        self.add_lines(self.long_hlines, self.fig, color='green')

    def plot_shorts(self):
        """
        """
        self.add_lines(self.short_hlines, self.fig, color='red')

    def plot_both(self):
        """
        """
        self.plot_longs()
        self.plot_shorts()


###########################################################################################
###########################################################################################

class PlotDaily(Plot2):
    """
    """
    def __init__(self, ut, n_days: int = 3, int_df=None, Untested=None, Interval=None, int_df=None, INTERVALS=None,
                 Interval=None, Interval=None, TestCandle=None, **kwargs):
        super().__init__(ut, **kwargs)
        self.n_days = n_days
        self.hcmins = int(n_days * 24 * 60)
        self.TC = TestCandle(Interval.in_1_minute, self.hcmins)
        self.HC = HoldCandle(Interval.in_daily, 3)
        self.name = self.HC.name

        self.df = self.HC.df
        self.long_hlines = None
        self.short_hlines = None
        self.fig = self.plot()

        for i in reversed(INTERVALS[1:]):
            n = int(round(self.hcmins / int_df.mins.loc[i]))
            if n > 5000:
                n = 5000
            hc = HoldCandle(Interval[i], n)
            ut = Untested(hc, self.TC)
            pc = PlotCandle(ut)
            print(pc.long_hlines)
            pc.long_hlines['interval'] = i
            pc.short_hlines['interval'] = i
            pc.long_hlines['color'] = int_df.c.loc[i]
            pc.short_hlines['color'] = int_df.c.loc[i]
            self.long_hlines = pd.concat([pc.long_hlines, self.long_hlines])
            print(self.long_hlines)
            self.short_hlines = pd.concat([pc.short_hlines, self.short_hlines])

    def add_holds(self, hlines, int_df=None, int_df=None):
        """
        """
        for i in int_df.index[1:]:
            df = self.long_hlines[self.long_hlines.interval == i]
            color = int_df.c.loc[i]
            print(color)
            for row in df.index:
                x0, y0, x1, y1 = df[['x0', 'y0', 'x1', 'y1']].loc[row].values
                self.fig.add_shape(type='line', line=dict(color=color),
                                   label=dict(text=y1, textposition='end', padding=0, font=dict(size=10),
                                              xanchor='right', yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

    def plot_longs(self):
        """
        """
        self.add_holds(self.long_hlines)

    def plot_shorts(self):
        """
        """
        self.add_holds(self.long_hlines)

    def plot_both(self):
        """
        """
        self.plot_longs()
        self.plot_shorts()


    ###################################################################################################################################################
class PlotAll(Plot2):
    """
    """
    def __init__(self, ut, n_days: int = 3, int_df=None, int_df=None, Untested=None, Interval=None, int_df=None,
                 INTERVALS=None, Interval=None, Interval=None, TestCandle=None, **kwargs):
        super().__init__(ut, **kwargs)
        self.n_days = n_days
        self.hcmins = int(n_days * 24 * 60)
        self.TC = TestCandle(Interval.in_1_minute, self.hcmins)
        self.HC = HoldCandle(Interval.in_daily, 3)
        self.name = self.HC.name

        self.df = self.HC.df
        self.long_hlines = None
        self.short_hlines = None
        self.fig = self.plot()

        for i in reversed(INTERVALS[1:]):
            n = int(round(self.hcmins / int_df.mins.loc[i]))
            if n > 5000:
                n = 5000
            hc = HoldCandle(Interval[i], n)
            ut = Untested(hc, self.TC)
            pc = PlotCandle(ut)
            print(pc.long_hlines)
            pc.long_hlines['interval'] = i
            pc.short_hlines['interval'] = i
            pc.long_hlines['color'] = int_df.c.loc[i]
            pc.short_hlines['color'] = int_df.c.loc[i]
            self.long_hlines = pd.concat([pc.long_hlines, self.long_hlines])
            print(self.long_hlines)
            self.short_hlines = pd.concat([pc.short_hlines, self.short_hlines])

    def add_holds(self, hlines, int_df=None, int_df=None):
        """
        """
        for i in int_df.index[1:]:
            df = self.long_hlines[self.long_hlines.interval == i]
            color = int_df.c.loc[i]
            print(color)
            for row in df.index:
                x0, y0, x1, y1 = df[['x0', 'y0', 'x1', 'y1']].loc[row].values
                self.fig.add_shape(type='line', line=dict(color=color),
                                   label=dict(text=y1, textposition='end', padding=0, font=dict(size=10),
                                              xanchor='right', yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

    def plot_longs(self):
        """
        """
        self.add_holds(self.long_hlines)

    def plot_shorts(self):
        """
        """
        self.add_holds(self.long_hlines)

    def plot_both(self):
        """
        """
        self.plot_longs()
        self.plot_shorts()
###################################################################################################################################################

class PlotAll2(Plot2):
    """
    """
    def __init__(self, uc, ut, int_df=None, int_df=None, Untested=None, Interval=None, int_df=None, INTERVALS=None,
                 **kwargs):
        super().__init__(ut, **kwargs)
        self.uc = uc
        self.name = self.uc.name
        self.hc = self.uc.holdcandle
        self.tc = self.uc.testcandle
        self.hcmins = self.uc.hcmins

        self.df = self.uc.df
        self.long_hlines = None
        self.short_hlines = None
        self.fig = self.plot()

        for i in reversed(INTERVALS[1:]):
            n = int(round(self.hcmins / int_df.mins.loc[i]))
            if n > 5000:
                n = 5000
            hc = HoldCandle(Interval[i], n)
            ut = Untested(hc, self.tc)
            pc = PlotCandle(ut)
            print(pc.long_hlines)
            pc.long_hlines['interval'] = i
            pc.short_hlines['interval'] = i
            pc.long_hlines['color'] = int_df.c.loc[i]
            pc.short_hlines['color'] = int_df.c.loc[i]
            self.long_hlines = pd.concat([pc.long_hlines, self.long_hlines])
            print(self.long_hlines)
            self.short_hlines = pd.concat([pc.short_hlines, self.short_hlines])

    def add_holds(self, hlines, int_df=None, int_df=None):
        """
        """
        for i in int_df.index[1:]:
            df = self.long_hlines[self.long_hlines.interval == i]
            color = int_df.c.loc[i]
            print(color)
            for row in df.index:
                x0, y0, x1, y1 = df[['x0', 'y0', 'x1', 'y1']].loc[row].values
                self.fig.add_shape(type='line', line=dict(color=color),
                                   label=dict(text=y1, textposition='end', padding=0, font=dict(size=10),
                                              xanchor='right', yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

    def plot_longs(self):
        """
        """
        self.add_holds(self.long_hlines)

    def plot_shorts(self):
        """
        """
        self.add_holds(self.long_hlines)

    def plot_both(self):
        """
        """
        self.plot_longs()
        self.plot_shorts()


###################################################################################################################################################

###########################################################################################
########################################################################################
