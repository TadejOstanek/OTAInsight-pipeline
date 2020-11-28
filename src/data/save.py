# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:27:21 2020
Module that deals with saving the data
@author: tadej
"""
from pathlib import Path
import os


def prepare_paths(year, hotel, foldername, filename, gzip=False):
    '''
    Prepare path for the file to be saved to
    Args:
        year (int): year data was shopped for
        hotel (str): name of the main hotel
        foldername (str): base folder where results are saved
        filename (str): name of particular file
        gzip (bool, optional): will the file be compressed as gzip
    Returns:
        pathlib.Path: full path to file in results folder
    '''
    extension = '.csv.gz' if gzip else '.csv'
    return (Path() / str(year) / foldername / hotel / 
        (filename + extension))


def save_export(data, year, hotel, foldername, filename, 
    gzip=False):
    '''
    Save the prepared export data. In case full path doesn't exist yet
    create the necessary folders
    Args:
        data (pd.DataFrame): ready results for save
        year (int): year the data was shopped for
        hotel (str): name of the main hotel
        foldername (str): base folder where results are saved
        filename (str): name of particular file
        gzip (bool, optional): compress the result as gzip
    Returns:
        pathlib.Path: folder where result was saved
    '''
    file = prepare_paths(year, hotel, foldername, filename, 
        gzip)
    folder = file.parents[0]

    if not os.path.isdir(folder):
        os.makedirs(folder)
    # infers compression from filename
    data.to_csv(file, index=False)
    return folder
