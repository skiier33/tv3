import pandas as pd

from CONSTANTS  import CSVS
from DataClass import FolderData
from data_funcs import get_hold_ixs

f = FolderData(CSVS)
df = f.__15
ixs =get_hold_ixs(df)

p=ixs.copy()
# prices = dict(longs=dict(fs:[], bs:[]), shorts=dict(fs:[], bs:[]))
for k in p.keys():
    hold = p[k]
    for bsfs in hold.keys():
        side = hold[bsfs]
        dfs = df.loc[side]

        if k == 'longs':
            prices = pd.concat([dfs.low, dfs.open])
        else:
            prices = pd.concat([dfs.high, dfs.open])

        d = {bsfs:prices}

        p[k].update(d)
        print(k, bsfs)


print('sdas')