# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:46:16 2020
API client for OTA insight.
@author: tadej
"""

from typing import Dict, List, Union, Optional
import datetime
import logging
from src.ota.baseapi import TokenAPI

logger = logging.getLogger(__name__)


class OTAInsight(TokenAPI):
    """
    Client for OTAInsight
    Params:
        token (str): access token from OTA
    Attributes:
        url (str): base url of the api endpoint
        response: placeholder for response of get requests
    Raises:
        TypeError-if token is not a string
    """
    URL = 'https://api.otainsight.com/v2/'

    def __init__(self, url=URL,
                 token=None):
        TokenAPI.__init__(self, url, token)

    def _get(self, endpoint='', **queryparams):
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
        self._response = self.response.json()

    @classmethod
    def init_from_file(cls, filepath, url=URL):
        '''
        Initialize a client by reading token from file
        Args:
            filepath (str): path to file with a token
        '''
        return super(OTAInsight, cls).init_from_file(
            filepath, url)

    def get_hotels(self):
        """Get data on all hotels the client is subscribed to
        Returns:
            list[dict]: dictionaries of hotel and its competitors
        """
        self._get(endpoint='hotels')
        return self.response['hotels']

    def get_rates(self, sub_id,
                  from_date,
                  ota='bookingdotcom',
                  los='1',
                  persons='2',
                  shop_length='90'):
        """
        Get rates data for a specified hotel
        Args:
            sub_id(str): subscription id of the hotel
            from_date(str|datetime.date): date from which to start
                %Y-%m-%d if string
            ota(str, optional): which ota channel to use
            los(int, optional): length of stay
            persons(int, optional): persons for stay
            shop_length(int, optional): how many days from start date
        Returns:
            list[dict]: one entry per day per hotel
        """

        self._get(endpoint='rates',
                  subscriptionId=sub_id, ota=ota, los=los,
                  persons=persons, fromDate=from_date,
                  shopLength=shop_length)
        return self.response['rates']
