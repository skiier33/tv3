from DataClass import Candle, Tester, Untapped
import copy
from tvDatafeed import Interval
import plotly.graph_objects as go


candle = Candle(Interval.in_15_minute, 20)

tester =  Tester(Interval.in_15_minute, 20, Interval.in_3_minute, 100)

l = tester.longs_untapped
s = tester.shorts_untapped
df = tester.df

copy(tester)


def plot_df(df, *args, **kwargs):

    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], \
                                     high=df['close'], low=df['low'], close=df['close'], \
                                     increasing_line_color='white', decreasing_line_color='cyan', \


                                     )])

    fig.update_layout(template= "plotly_dark", xaxis_rangeslider_visible=False,  **kwargs)

    return fig



fig = plot_df(candle.df, title=f'{candle.name}', plot_bgcolor='black')
h = candle.long_alines['alines']
for i in h:
    fig.add_shape(x0=h[0], y0=h[1])

# fig.update_yaxes(showgrid=False, tickfont=dict(family='Rockwell', color='black'))
fig.show()


print('dsafads')
