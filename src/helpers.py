# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:27:21 2020
various functions used by the main process
@author: tadej
"""
import pandas as pd
import numpy as np
import re
from pathlib import Path
from datetime import datetime, date
import os


def generate_dates(today):
    '''generate for which starting dates an export will be made'''
    start_date = today.replace(month=3, day=1)
    start_date_next = start_date.replace(year=start_date.year + 1)

    if today.month == 12:
        sdates = [start_date_next]
    elif today.month >= 10:
        sdates = [start_date, start_date_next]
    else:
        sdates = [start_date]
    return sdates


def prep_data(plist, date_stamp):
    '''prepare the data for save'''

    rates_data = pd.concat(plist).reset_index().rename(
        columns={'level_0': 'site'}).drop(columns='level_1')
    rates_data['date_stamp'] = str(date_stamp)

    rates_data = rates_data.loc[:, ['date_stamp', 'site', 'arrivalDate',
                                    'hotelName', 'value']]

    rates_data = rates_data.assign(
        value=rates_data.value.replace(0, np.nan))
    return rates_data


def save_export(data, year, hotel, fname, sfolder, compression=None):
    '''save the export file'''
    folder = Path()
    folder = folder / year / sfolder / hotel
    file = folder / fname

    if compression == 'gzip':
        file = file.with_suffix('.csv.gz')
    else:
        file = file.with_suffix('.csv')

    for _ in range(2):
        try:
            data.to_csv(file, index=False, compression=compression)
        except FileNotFoundError:
            os.makedirs(folder)
        else:
            break
    return folder


def combine_csvs(export_folder):
    '''combine select csvs in the export folder of the hotel'''
    dfs = list()
    for root, folder, files in os.walk(export_folder):
        for file in files:
            try:
                date_parse = datetime.strptime(
                    re.search(
                        r'\d{4}-\d{2}-\d{2}', file)[0], '%Y-%m-%d').date()
            # no date in file name - initial export
            except TypeError:
                day_diff = 0
            else:
                day_diff = (date.today() - date_parse).days

            if day_diff <= 7 or date_parse.day in [7, 14, 21, 30]:
                dfs.append(pd.read_csv(export_folder / file))
    return pd.concat(dfs)
