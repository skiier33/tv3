import plotly.graph_objects as go
import pandas as pd

1
import plotly.graph_objects as go
import pandas as pd
from DataClass import HoldCandle



class BasePlot(HoldCandle):
    """
    Plots hold levels before testing
    """

    def __init__(self, interval, n_bars):
        super().__init__(interval, n_bars)
        self.long_hlines = self.get_long_hlines()
        self.short_hlines = self.get_short_hlines()
        self.fig = self.plot()



    def get_long_hlines(self)->pd.DataFrame:

        long_hlines = pd.DataFrame(self.longs)
        long_hlines['x1'] = self.df.index[-1]
        long_hlines['y1'] = long_hlines[0]
        long_hlines.index.name='x0'
        long_hlines = long_hlines.reset_index()


        return long_hlines.rename(columns={0:'y0'})
    
    def get_short_hlines(self)->pd.DataFrame:

        short_hlines = pd.DataFrame(self.shorts)
        short_hlines['x1'] = self.df.index[-1]
        short_hlines['y1'] = short_hlines[0]
        short_hlines.index.name='x0'
        short_hlines = short_hlines.reset_index()


        return short_hlines.rename(columns={0:'y0'})

    def plot(self):

        fig = go.Figure(data=[go.Candlestick(x=self.df.index,
                        open=self.df['open'], high=self.df['high'],
                        low=self.df['low'], close=self.df['close'])], layout=go.Layout())

        fig.update_layout(title=self.name, xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price', template="plotly_dark")

        # fig.update_traces(name='fff',  selector = dict(type='candlestick'))

        fig.update_traces(increasing_line_color= 'white', selector = dict(type='candlestick'))

        fig.update_traces(decreasing_line_color= 'blue', selector = dict(type='candlestick'))

        for row in self.long_hlines.index:
           x0, y0, x1, y1 = self.long_hlines.loc[row].values
           fig.add_shape(type='line', line=dict(color='green'), label=dict(text=y1, textposition='end', padding=0, font=dict(size=10), xanchor='right', yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

        for row in self.short_hlines.index:
           x0, y0, x1, y1 = self.short_hlines.loc[row].values
           fig.add_shape(type='line', line=dict(color='red'), label=dict(text=y1, textposition='end', padding=0, font=dict(size=10), xanchor='right', yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

        return fig






class UntestedPlot:
    def __init__(self,df,  **kwargs):

        self.df = df
        self.kwargs = kwargs

        self.long_hlines = self.get_long_hlines()
        self.short_hlines = self.get_short_hlines()
        self.fig = self.plot()



    def get_long_hlines(self) -> pd.DataFrame:

        long_hlines = pd.DataFrame(self.kwargs['untested_longs'])
        long_hlines['x1'] = self.df.index[-1]
        long_hlines['y1'] = long_hlines[0]
        long_hlines.index.name = 'x0'
        long_hlines = long_hlines.reset_index()

        return long_hlines.rename(columns={0: 'y0'})

    def get_short_hlines(self) -> pd.DataFrame:

        short_hlines = pd.DataFrame(self.kwargs['untested_shorts'])
        short_hlines['x1'] = self.df.index[-1]
        short_hlines['y1'] = short_hlines[0]
        short_hlines.index.name = 'x0'
        short_hlines = short_hlines.reset_index()

        return short_hlines.rename(columns={0: 'y0'})

    def plot(self):

        fig = go.Figure(data=[go.Candlestick(x=self.df.index,
                                             open=self.df['open'], high=self.df['high'],
                                             low=self.df['low'], close=self.df['close'])], layout=go.Layout())


        fig.update_layout(title= self.kwargs['holdcandle'].name,  xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price',
                          template="plotly_dark")

        # fig.update_traces(name='fff',  selector = dict(type='candlestick'))

        fig.update_traces(increasing_line_color='white', selector=dict(type='candlestick'))

        fig.update_traces(decreasing_line_color='blue', selector=dict(type='candlestick'))

        for row in self.long_hlines.index:
            x0, y0, x1, y1 = self.long_hlines.loc[row].values
            fig.add_shape(type='line', line=dict(color='green'),
                          label=dict(text=y1, textposition='end', padding=0, font=dict(size=10), xanchor='right',
                                     yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

        for row in self.short_hlines.index:
            x0, y0, x1, y1 = self.short_hlines.loc[row].values
            fig.add_shape(type='line', line=dict(color='red'),
                          label=dict(text=y1, textposition='end', padding=0, font=dict(size=10), xanchor='right',
                                     yanchor='middle'), x0=x0, y0=y0, x1=x1, y1=y1)

        return fig
