# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:46:16 2020
API client for OTA insight.
@author: tadej
"""

from typing import Dict, List, Union, Optional
import datetime
import logging
import requests
from src.ota.baseapi import TokenAPI

logger = logging.getLogger(__name__)


class OTAInsight(TokenAPI):
    """
    Client for OTAInsight
    """
    URL = 'https://api.otainsight.com/v2/'

    def __init__(self, url: str = URL,
        token: Optional[str] = None):
        """
        Initialize the class with auth token
        Args:
            token (str): access token from OTA
        """
        TokenAPI.__init__(self, url, token)

    def _get(self, endpoint: str = '', **queryparams) -> Dict:
        """
        Handle authenticated GET requests - extend parent
        by taking the parsed response as dictionary
        Args:
            endpoint (str, optional):
                the api folder to append to base url
            queryparams (**kwargs): The query string parameters
        """
        super(OTAInsight, self)._get(
            endpoint=endpoint, **queryparams)
        self.response = self.response.json()

    @classmethod
    def init_from_file(cls, filepath, url=URL):
        '''calls parent class method but adds url'''
        return super(OTAInsight, cls).init_from_file(
            filepath, url)

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
