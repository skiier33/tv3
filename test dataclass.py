
from CONSTANTS import  CSVS
import pathlib
import pandas as pd
import numpy as np
from data_funcs import parse_csv




class CsvReader:
    def __init__(self, csv_folder: str) -> None:
        self.csv_folder = pathlib.Path(csv_folder)
        self.files = list(self.csv_folder.glob('*.csv'))

        for file in self.files:
            self.name = file.parts[-1].split(' ')[-1].split('_')[0]
            self.df = parse_csv(file)
            self.__setattr__(f'__{self.name}', self.df)


r = CsvReader(CSVS)

print('jjjj')