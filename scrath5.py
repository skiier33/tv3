from DataClass import *
from CONSTANTS import  *


reader = CsvReader(csvs_path)

tf = TimeFrame(reader.__getattribute__)
hc = HoldCandle(tf)


hn = 60

for i in int_df.int.loc[int_df.min<hn]:
    lows = reader.__dict__[int_df[i]].low
    highs = reader.__dict__[int_df[i]].high
    hc.longs =  test_holds(hc.longs, lows)
    hc.shorts =  test_holds(hc.shorts, highs)


print('sdfds')
