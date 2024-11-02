
import pandas as pd
import pathlib

from CONSTANTS  import CSVS
from DataClass import FolderData, TimeFrameData, TimeFramePlot
from data_funcs import get_data, update_data, plot_df,  test_holds, get_hlines, plot_df, add_hold_lines, read_binance_csv,  test_long_hold
import plotly.graph_objects as go
import datetime
import ccxt

csv_folder =pathlib.Path(r"C:\Users\akrug\PycharmProjects\pythonProject2\test data")
files = pd.Series(csv_folder.glob('*.csv'))


# since = datetime.datetime.now() - datetime.timedelta(days=7)
# df  = get_data(since, timeframe='1h')

hold_tf = TimeFrameData(read_binance_csv(files[1]))
hold_tf.get_untested()

tfp = TimeFramePlot(hold_tf)


test = read_binance_csv(files[2])
test = TimeFrameData(test)

print(f'testing {hold_tf.name},start: {hold_tf.start} bars: {hold_tf.n_bars} with {test.name} start = {test.start}')

ut_longs= test_long_hold(hold_tf.longs, test.df)
ut2 = test_long_hold(hold_tf.longs.round(1), test.df)
ut3 = test_long_hold(hold_tf.longs.round(0), test.df)
ut4 = test_long_hold(hold_tf.longs.round(0), test.df.round(1))
ut5 = test_long_hold(hold_tf.longs.round(0), test.df.round(0))
# ut_longs= test_long_hold(hold_tf.longs, test.df)



print('sdas')


