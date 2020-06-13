# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:53:04 2020

@author: tadej
"""

from pathlib import Path
import pandas as pd
import numpy as np
import os

project = 'Kalyves Beach Hotel'

placeholder = list()
for root, dirs, files in os.walk(Path("past_from_excel/" + project)):
    for file in files:
        if file.endswith('.csv'):
            site = file[:file.index('_'):]
            hotel = file[file.index('_') + 1:file.index('.csv')]
            data = pd.read_csv(Path('past_from_excel/' + project, file),
                               parse_dates=['Date'], dayfirst=True)
            data = data.assign(Date=data.Date.dt.date)

            data = data.melt('Date')
            data = data.rename(columns={'Date': 'arrivalDate',
                                        'variable': 'date_stamp'})
            data.insert(2, 'hotelName', hotel)
            data.insert(2, 'site', site)
            # drop all snapshots in the future
            data = data.loc[~data.value.isna()]

            data = data.assign(value=data.value.replace(
                'Sold out', np.nan).replace('No data', np.nan).astype(float))
            placeholder.append(data)

alldata = pd.concat(placeholder, sort=False)
alldata.to_csv(Path(
    'data_export/' + project + '/rates_result_past.csv'),
    index=False)
