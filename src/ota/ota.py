# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:46:16 2020
API client for OTA insight.
@author: tadej
"""

from typing import Dict, List, Union
import datetime
import logging
import requests

logger = logging.getLogger(__name__)

class OTAInsight:
    """
    Client for OTAInsight
    """

    URL = "https://api.otainsight.com/v2/"

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

        self._token = auth_token
        self._session = requests.Session()
        self.response = None

    @property
    def token(self):
        '''Make token a read only property'''
        return self._token

    @property
    def session(self):
        '''Make session a read only property'''
        return self._session

    @classmethod
    def init_from_file(cls, filepath: str):
        ''' Initialize the client by providing the path to the token

        Args:
            filepath(str): filepath to token
        '''
        with open(filepath, 'r') as file:
            return cls(file.read())

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
        Handle authenticated GET requests, works for non
        string arguments as long as they can be turned to string

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
            url=OTAInsight.URL + folder, params=params)
        response.raise_for_status()
        logger.info('Sucessfully retrieved from %s', folder)
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
                  shop_length: Union[str, int] = '90') -> List[Dict]:
        """
        Get rates data for a specified hotel

        Args:
            sub_id(str): subscription id of the hotel
            from_date(str_or_datetime.date): date from which to start
                %Y-%m-%d if string
            ota(str, optional): which ota channel to use
            los(str_or_int, optional): length of stay
            persons(str_or_int, optional): persons for stay
            shop_length(str_or_int, optional): how many days from start date

        Returns:
            list_of_dict: one entry per day per hotel
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

    Raises:
        TypeError: in case floats are passed
    '''
    if [el for el in qparams.values() if isinstance(el, float)]:
        raise TypeError('query parameters cannot be floats')
    return {key: str(val) for key, val in qparams.items()}
