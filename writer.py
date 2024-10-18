import copy
from tvDatafeed import TvDatafeed, Interval
import pickle
username = 'Fook_Yew'
password = 'Tr4d1ng1sc00l'
tv = TvDatafeed(username, password)


from datafuncs import Candle, HoldTest, ut2
from tvDatafeed import  Interval


ht = HoldTest(Interval.in_15_minute, 100, Interval.in_1_minute, 1500)

untapped_longs = ht.untapped_longs
untapped_shorts = ht.untapped_shorts
hold_candle = ht.hold_candle

hold_candle = ht.hold_candle

import pickle

# Create a variable
myvars = [ht, hold_candle, untapped_longs, untapped_shorts]

# Open a file and use dump()
with open('file.pkl', 'wb') as file:
    # A new file will be created
    for var in myvars:
        pickle.dump(var, file)
print('pickled at the untapped levels')