# coding=utf-8
"""
Base API class logic, to be shared among various projects
to get a headstart with implementation and testing
"""
import logging
import requests
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)

class BaseAPI:
    '''Base class for other API clients to build on'''

    def __init__(self, url):
        '''
        Return instance of class
        Args:
            url(str): base url of the api
        '''

        self._url = url
        self._session = requests.Session()
        self.response = None
        self._session.mount(self._url, HTTPAdapter(max_retries=5))

    @property
    def url(self):
        return self._url

    @property
    def session(self):
        return self._session
    
    def _get(self, endpoint='', **queryparams):
        '''
        Handle authenticated GET requests. Can handle non-string
        query params as long as they can be converted to string
        Args:
            endpoint (str, optional): extra path for a particualar 
                API endpoint
            queryparams (**kwargs): http query parameters
        Raises:
            requests.exceptions.HTTPError for error status codes
        '''
        self.response = self.session.get(
            url=self.url + endpoint, params=queryparams,
            timeout=3)
        self.response.raise_for_status()
        logger.info(
            'Sucessfully retrieved from %s%s', self.url, endpoint)