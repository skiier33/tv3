import datetime

from CONSTANTS import  CSVS
import pathlib
import pandas as pd
import numpy as np
from data_funcs import read_binance_csv
import re




class FolderData:
    """Create an object of dataframes for all csvs in a folder

    """
    def __init__(self, csv_folder: str,*args, **kwargs) -> None:
        self.csv_folder = pathlib.Path(csv_folder)
        self.files = list(self.csv_folder.glob('*.csv'))

        for file in self.files:
            self.name = file.parts[-1].split('.')[0]
            self.df = TimeFrameData(read_binance_csv(file))

            self.__setattr__(f'__{self.name}', self.df)


class TimeFrameData:
    def __init__(self,df:pd.DataFrame) -> None:
        self.df = df
        self.dt = df.index[1] - df.index[0]
        self.name = str(self.dt)
        self.n_bars = int(len(df))
        self.df['up_down'] = np.sign(self.df.close - self.df.open)
        self.df.sort_index(inplace=True)

        self.long_indexs = []
        self.short_indexs = []
        self.longs = None
        self.shorts = None


    def round_df(self):
       # self.df =  self.df.round(digits)
       return self.df.round(self.round_digits)

        # self.get_untested()

    def get_untested(self):
        for time in self.df.index[:-4]:

            try:


                t2 = self.df.index.get_loc(time)+3
            except(TypeError):
                print(f'type error at {time}')
                t2a = time + 3*self.dt
                continue
            sl = slice(time, self.df.index[t2])
            chunk = self.df.loc[sl]
            try:
                if all(chunk['up_down'] ==  [1, 1, -1, -1]):
                    self.short_indexs.extend(chunk.index[:2])
                elif all(chunk['up_down'] ==  [-1,-1, 1, 1]):
                    self.long_indexs.extend(chunk.index[:2])

            except(ValueError):
                print(f'Valeue error at {time}')

                continue


        self.longs = pd.concat([self.df['open'].loc[self.long_indexs], self.df['high'].loc[self.long_indexs]]).sort_index()
        self.shorts = pd.concat([self.df['open'].loc[self.short_indexs], self.df['low'].loc[self.short_indexs]]).sort_index()

        #






