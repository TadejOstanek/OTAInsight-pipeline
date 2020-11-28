# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:27:21 2020
Module that deals with preparing the data to right format
@author: tadej
"""
import pandas as pd
import numpy as np


def concat_dict_to_pd(pdict):
    '''
    Combine a dictionary of lists into a pandas dataframe with 
    one of the columns dict keys
    Args:
        pdict (dict): a dictionary with entry for each source
    Returns:
        pd.DataFrame: all data combined with site column
    '''
    pdict = {key: pd.DataFrame(el) for key, el in pdict.items()}
    rates_data = pd.concat(
        pdict, names=['site', 'drop']).reset_index()
    return rates_data

def prep_data(pdict, date_stamp):
    '''prepare the data for save'''
    pdict = {key: pd.DataFrame(el) for key, el in pdict.items()}
    rates_data = pd.concat(pdict).reset_index().rename(
        columns={'level_0': 'site'}).drop(columns='level_1')
    rates_data['date_stamp'] = str(date_stamp)

    rates_data = rates_data.loc[:, ['date_stamp', 'site', 'arrivalDate',
                                    'hotelName', 'value']]

    rates_data = rates_data.assign(
        value=rates_data.value.replace(0, np.nan))
    return rates_data
