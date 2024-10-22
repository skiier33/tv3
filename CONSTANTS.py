import pathlib

from tvDatafeed import TvDatafeed
import pandas as pd

CSVS = pathlib.WindowsPath(r'C:/Users/akrug/PycharmProjects/pythonProject2/data').absolute()

username = 'Fook_Yew'
password = 'Tr4d1ng1sc00l'
tv = TvDatafeed(username, password)


INTERVALS = ['in_1_minute', 'in_3_minute', 'in_5_minute', 'in_15_minute', 'in_1_hour', 'in_4_hour', 'in_daily']
COLORS = ['grey', 'pink', 'green', 'orange', 'blue', 'yellow', 'red']
csv_key = ['__1__','__3__','__5__', '__15__', '__60__', '__1D__', '__1W__']
MINS = [1,3,5,15,60,240,1440]


d = {'int':INTERVALS, 'csv':csv_key, 'c': COLORS, 'mins':MINS}
int_df = pd.DataFrame.from_dict(d)
int_df.index = int_df['int']
