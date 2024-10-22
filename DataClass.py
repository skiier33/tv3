import pathlib
from typing import List, Any

import pandas as pd
import numpy as np

#################################################
#################################################


p =r'C:/Users/akrug/PycharmProjects/pythonProject2/data'



class CsvReader:
    def __init__(self, csv_folder: str)->None:
        self.csv_folder = pathlib.Path(csv_folder)
        self.files = list(self.csv_folder.glob('*.csv'))

        for file in self.files:
            name = file.parts[-1].split(' ')[-1].split('_')[0]
            self.__setattr__(f'__{name}', {str(name)}')

#################################################

#################################################

###################################################################################################
