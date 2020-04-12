# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:46:16 2020
API client for OTA insight.
@author: tadej
"""

import requests
import pandas as pd


class OTAInsight:
    """
    Client for OTAInsight
    """
    def __init__(self, auth_token=None):
        """
        Initialize the class with auth token
        :param auth_token: access token
        :type access_token: :py:class:`str`
        """
        if auth_token is None:
            raise Exception('You must provide an OAuth access token')
        self.token = auth_token
        self.url = "https://api.otainsight.com/v2/"


    def _get(self, folder, **queryparams):
        """
        Handle authenticated GET requests
        :param folder: the sub-api to get from hotels/rates
        :param queryparams: The query string parameters
        :returns: The JSON output from the API
        """
        params = {'token': self.token}
        if len(queryparams):
            params.update(queryparams)
        try:
            response = requests.get(url=self.url + folder, params=params)
        except requests.exceptions.RequestException as e:
            raise e
        else:

            return response.json()

    def get_hotels(self):
        """Get data on all hotels the client is subscribed to."""

        return self._get(folder='hotels')['hotels']

    def get_rates(self, sub_id, ota='bookingdotcom', los='1', persons='2',
                  from_date='', shop_length='90'):
        """
        Get rates data.

        Args
        ----
        sub_id: subscription id of the hotel
        ota: which ota channel to use
        los: length of stay
        persons: persons for stay
        from_date: from which date to return the data yyyy-mm-dd
        shop_length: how many days from start date to return
        """

        result = self._get(folder='rates',
                         subscriptionId=sub_id, ota=ota, los=los,
                         persons=persons, fromDate=from_date,
                         shopLength=shop_length)['rates']

        return pd.DataFrame(result)



