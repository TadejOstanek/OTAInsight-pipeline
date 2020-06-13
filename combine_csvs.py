# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:41:35 2020

@author: tadej
"""

import os
from pathlib import Path
import re
from datetime import datetime, date
import pandas as pd

for hotel in ['Kalyves Beach Hotel',
              'Kiani Beach Resort Family All Inclusive']:

    dfs = list()

    for root, folder, files in os.walk(Path('data_export', hotel)):
        for file in files:
            try:
                date_parse = datetime.strptime(
                    re.search(r'\d\d\d\d-\d\d-\d\d', file)[0], '%Y-%m-%d').date()
            # no date in file name
            except TypeError:
                day_diff = 0
            else:
                day_diff = (date.today() - date_parse).days

            if day_diff <= 7 or day_diff % 7 == 0:
                dfs.append(pd.read_csv(Path('data_export', hotel, file)))

    all_data = pd.concat(dfs)

    all_data.to_csv(Path('results', hotel, 'all_data.csv'), index=False)
