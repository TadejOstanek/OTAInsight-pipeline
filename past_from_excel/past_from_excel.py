# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:53:04 2020

@author: tadej
"""

from pathlib import Path
import pandas as pd
import os

for root, dirs, files in os.walk(Path("past_from_excel")):
    for file in files:
        if not file.endswith('.py'):
            datest = file[:file.index('.csv')]
            data = pd.read_csv(Path('past_from_excel', file),
                               parse_dates=['Date'], dayfirst=True)
            data = data.assign(Date=data.Date.dt.date)

            data = data.melt('Date')
            data = data.rename(columns={'Date': 'arrivalDate',
                                        'variable': 'hotelName'})
            data.insert(0, 'date_stamp', datest)
            data = data.assign(value=data.value.replace(
                'Sold out', '0').astype(float))

            data.to_csv(Path('data_export/rates_result' + datest + '.csv'),
                        index=False)
