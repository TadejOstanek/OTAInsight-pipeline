# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:27:21 2020
Module that deals with preparing the data to right format
@author: tadej
"""
import pandas as pd
import numpy as np


def concat_dict_to_pd(api_res):
    '''
    Combine a dictionary of lists into a pandas dataframe with
    one of the columns dict keys
    Args:
        api_res (dict): a dictionary with entry for each source
    Returns:
        pd.DataFrame: all data combined with site column
    '''
    api_res = {key: pd.DataFrame(el) for key, el in api_res.items()}
    data = pd.concat(
        api_res, names=['site', 'drop']).reset_index()
    return data


def prep_data(api_res, date_stamp):
    '''
    Prepare API resutlt data for save as a csv
    Args:
        api_res (dict):  a dictionary with entry for each source
        date_stamp (datetime.date): date of data capture
    Returns:
        pd.DataFrame: data ready for save
    '''
    rates_data = concat_dict_to_pd(api_res)
    rates_data.loc[:, 'date_stamp'] = date_stamp
    rates_data = rates_data.loc[
        :, ['date_stamp', 'site', 'arrivalDate',
            'hotelName', 'value']]
    rates_data.value.replace(0, np.nan, inplace=True)
    return rates_data
