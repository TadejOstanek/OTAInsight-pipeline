# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:27:21 2020
Module that deals with saving the data
@author: tadej
"""
from pathlib import Path
import os


def save_export(data, year, hotel, fname, sfolder, compression=None):
    '''save the export file'''
    folder = Path(os.getcwd()).parent
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
