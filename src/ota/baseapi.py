# coding=utf-8
"""
Base API class logic, to be shared among various projects
to get a headstart with implementation and testing
"""
import os
import logging
import requests
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)


class BaseAPI:
    '''
    Base class for other API clients to build on
    Params:
        url(str): base url of the api
    Attributes:
        url (str): base url of the api endpoint
        response: placeholder for response of get requests
    '''

    def __init__(self, url):
        self._url = url
        self._session = requests.Session()
        self._response = None
        self._session.mount(self._url, HTTPAdapter(max_retries=5))

    @property
    def url(self):
        '''set url as property'''
        return self._url

    @property
    def response(self):
        '''response as property'''
        return self._response
    

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
        self._response = self._session.get(
            url=self.url + endpoint, params=queryparams,
            timeout=3)
        self.response.raise_for_status()
        logger.info(
            'Sucessfully retrieved from %s%s', self.url, endpoint)


class TokenAPI(BaseAPI):
    '''
    Extension of base api that uses a simple token for auth.
    It can read it from environmantal variables
    Params:
        url(str): base url of the api
        token(str, optional): auth token
    Attributes:
        url (str): base url of the api endpoint
        response: placeholder for response of get requests
    ClassMethods:
        init_from_file: initialize an instance by passing
            the path to token txt file
    Raises:
        TypeError-if token is not a string
    '''

    def __init__(self, url, token=None):
        BaseAPI.__init__(self, url)
        if token is None:
            token = os.environ.get('OTATOKEN')
        if not isinstance(token, str):
            raise TypeError(
                'You must provide a valid access token')
        self._token = token

    @classmethod
    def init_from_file(cls, filepath, url):
        ''' Initialize the client by providing the path to the token
        Args:
            filepath (str): filepath to token
            url (str): base url for the api
        '''
        with open(filepath, 'r') as file:
            return cls(url, token=file.read())

    def _get(self, endpoint='', **queryparams):
        """
        Handle authenticated GET requests
        Extend parent by passing token to query parameters
        Args:
            endpoint (str, optional):
                the api folder to append to base url
            queryparams (**kwargs): The query string parameters
        """
        super()._get(endpoint=endpoint,
                     token=self._token, **queryparams)
