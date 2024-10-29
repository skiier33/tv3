
import pandas as pd
import pathlib

from CONSTANTS  import CSVS
from DataClass import FolderData, TimeFrameData
from data_funcs import get_data, update_data, plot_df,  test_holds, get_hlines, plot_df, add_hold_lines, read_binance_csv,  test_long_hold, test_short_hold
import plotly.graph_objects as go
import datetime
import ccxt

csv_folder =pathlib.Path(r'C:\Users\akrug\PycharmProjects\pythonProject3\data_2024')
files = pd.Series(csv_folder.glob('*.csv'))




hold_tf = TimeFrameData(read_binance_csv(files[1]))
hold_tf.get_untested()

p = pathlib.Path(r'C:\Users\akrug\PycharmProjects\pythonProject3\data_2024')

ut_longs= test_long_hold(hold_tf, p)


ut_short = test_short_hold(hold_tf,p)


print('sdas')


