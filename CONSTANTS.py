import pandas as pd

INTERVALS = ['in_1_minute', 'in_3_minute', 'in_5_minute', 'in_15_minute', 'in_1_hour', 'in_4_hour', 'in_daily']
COLORS = ['grey', 'pink', 'green', 'orange', 'blue', 'yellow', 'red']
N_BARS = [1000, 300, 200, 100, 40, 20, 10]

d = {'int':INTERVALS,'n': N_BARS, 'c': COLORS}
df = pd.DataFrame.from_dict(d)
df.index = df['int']
