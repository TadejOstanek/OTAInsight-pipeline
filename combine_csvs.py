# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:41:35 2020

@author: tadej
"""

import os
from pathlib import Path
import pandas as pd

dfs = list()
for root, folder, files in os.walk(Path('data_export')):
    for file in files:
        dfs.append(pd.read_csv('data_export/' + file))

all_data = pd.concat(dfs)

all_data.to_csv('all_data.csv', index=False)
