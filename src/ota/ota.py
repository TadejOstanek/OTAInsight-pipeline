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
from src.ota.baseapi import BaseAPI

logger = logging.getLogger(__name__)


class OTAInsight(BaseAPI):
    """
    Client for OTAInsight
    """

    URL = 'https://api.otainsight.com/v2/'

    def __init__(self, auth_token: str):
        """
        Initialize the class with auth token

        Args:
            auth_token (str): access token from OTA

        Raises:
            TypeError-if token is not a string
        """
        BaseAPI.__init__(self, OTAInsight.URL)
        if not isinstance(auth_token, str):
            raise TypeError(
                'You must provide a valid OAuth access token')

        self._token = auth_token

    @property
    def token(self):
        '''Make token a read only property'''
        return self._token

    @classmethod
    def init_from_file(cls, filepath: str):
        ''' Initialize the client by providing the path to the token

        Args:
            filepath(str): filepath to token
        '''
        with open(filepath, 'r') as file:
            return cls(file.read())

    def _get(self, endpoint: str = '', **queryparams) -> Dict:
        """
        Handle authenticated GET requests, works for non
        string arguments as long as they can be turned to string

        Args:
            endpoint (str, optional):
                the api folder to append to base url
            queryparams (**kwargs): The query string parameters

        Raises:
            requests.exceptions.HTTPError for error status codes
        """
        super(OTAInsight, self)._get(endpoint=endpoint, 
            token=self.token, **queryparams)
        self.response = self.response.json()

    def get_hotels(self) -> List[Dict]:
        """Get data on all hotels the client is subscribed to

        Returns:
            list: dictionaries of hotel and its competitors
        """
        self._get(endpoint='hotels')
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

        self._get(endpoint='rates',
                  subscriptionId=sub_id, ota=ota, los=los,
                  persons=persons, fromDate=from_date,
                  shopLength=shop_length)
        return self.response['rates']
