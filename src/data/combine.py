# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:27:21 2020
Module that deals with combining multiple csv
into one ready for excel imprt
@author: tadej
"""
import pandas as pd
import re
from datetime import datetime, date
import os


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
