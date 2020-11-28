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


def detect_required_files(folder):
    '''Detect which files should be combined. 
    Business logic is all in last week and specific dates each month
    Args:
        folder (patlib.Path): folder where results are located
    Returns:
        list: list of full file names to read
    '''
    file_list = []
    # cannot do a comprehension due to error catch
    for root, folder, files in os.walk(folder):
        for file in files:
            try:
                date_parse = datetime.strptime(
                    re.search(
                        r'\d{4}-\d{2}-\d{2}', file)[0], '%Y-%m-%d').date()
            # no date in file name - initial export
            except TypeError:
                file_list.append(file)
            else:
                if (date.today() - date_parse).days <= 7 or (
                    date_parse.day in [7, 14, 21, 30]):
                    file_list.append(file)
    return file_list

def combine_csvs(export_folder):
    '''combine select csvs in the export folder of the hotel'''
    files = detect_required_files(export_folder)
    result = pd.concat(
        [pd.read_csv(export_folder / file) for file in files],
        sort=False).reset_index(drop=True)
    return result
