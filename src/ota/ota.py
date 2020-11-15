# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:46:16 2020
API client for OTA insight.
@author: tadej
"""

from typing import Dict, List, Union
import datetime
import requests


class OTAInsight:
    """
    Client for OTAInsight
    """

    def __init__(self, auth_token: str):
        """
        Initialize the class with auth token

        Args:
            auth_token (str): access token from OTA

        Raises:
            TypeError-if token is not a string
        """
        if not isinstance(auth_token, str):
            raise TypeError(
                'You must provide a valid OAuth access token')

        self.token = auth_token
        self.url = "https://api.otainsight.com/v2/"
        self.session = requests.Session()
        self.response = None

    @classmethod
    def init_from_file(cls, filepath: str):
        ''' Initialize the client by providing the path to the token
        
        Args:
            filepath(str): filepath to token
        '''
        with open(filepath, 'r') as f:
            return cls(f.read())


    def _append_token(self, qparams: Dict) -> Dict:
        '''Append token to other query parameters for get

        Args:
            qparams(dict): dictionary of additional query
                parameters. Can be empty

        Returns:
            dict: query parameters with added token

        Raises:
            TypeError-if input not dictionary
        '''
        if not isinstance(qparams, dict):
            raise TypeError('extra query parameters should be '
                            'in a dictionary')

        qparams.update({'token': self.token})
        return qparams


    def _get(self, folder: str = '', **queryparams) -> Dict:
        """
        Handle authenticated GET requests

        Args:
            folder (str, optional):
                the api folder to append to base url
            queryparams (**kwargs): The query string parameters

        Raises:
            requests.exceptions.HTTPError for error status codes
        """
        params = query_params_to_str(queryparams)
        params = self._append_token(params)
        response = self.session.get(
            url=self.url + folder, params=params)
        response.raise_for_status()
        self.response = response.json()

    def get_hotels(self) -> List[Dict]:
        """Get data on all hotels the client is subscribed to

        Returns:
            list: dictionaries of hotel and its competitors
        """
        self._get(folder='hotels')
        return self.response['hotels']

    def get_rates(self, sub_id: str,
                  from_date: Union[str, datetime.date],
                  ota: str = 'bookingdotcom',
                  los: Union[str, int] = '1',
                  persons: Union[str, int] = '2',
                  shop_length: Union[str, int] = '90'):
        """
        Get rates data for a specified hotel

        Args:
            sub_id(str): subscription id of the hotel
            from_date(str_or_datetime.date): date from which to start
                %Y-%m-%d if string
            ota(str): which ota channel to use
            los(str_or_int): length of stay
            persons(str_or_int): persons for stay
            shop_length(str_or_int): how many days from start date
        """

        self._get(folder='rates',
                  subscriptionId=sub_id, ota=ota, los=los,
                  persons=persons, fromDate=from_date,
                  shopLength=shop_length)
        return self.response['rates']


def query_params_to_str(qparams: Dict) -> Dict:
    '''Turn extra query parameters to strings

    Args:
        qparams(dict): dictionary of additional query
        parameters. Can be empty

    Returns:
        dict: query parameters with values as strings
    '''
    if [el for el in qparams.values() if isinstance(el, float)]:
        raise TypeError('query parameters cannot be floats')
    return {key: str(val) for key, val in qparams.items()}
