'''
Test OTAInsight API client
'''
from datetime import date
import os
import pytest
import requests
import requests_mock
from src.ota.ota import OTAInsight
from src.ota.baseapi import TokenAPI

@pytest.fixture(scope='module')
def client():
    '''Fixture to use the samle client and session
    for all tests'''
    return OTAInsight(token='test_token')


class TestInit:
    '''Test the __init__ constructor of the class'''

    def test_implements_base_class(self, client):
        '''Make sure attributed are assigned correctly'''
        assert isinstance(client, TokenAPI)
        assert client.token == 'test_token'

    def test_url(self, client):
        '''test if the url is set automatically'''
        assert client.url == 'https://api.otainsight.com/v2/'


class TestInitFromFile:
    '''Test class method that initializes class by providing a path 
    to where the token is'''

    @pytest.fixture()
    def create_token_file(self, tmpdir):
        '''Creates temp txt with token'''
        tokenpath = tmpdir.join('test_token.txt')
        with open(tokenpath, 'w') as t:
            t.write('testtokenvalue')
        yield tokenpath
        os.remove(tokenpath)

    def test_generates_client(self, create_token_file):
        tokenpath = create_token_file
        client = OTAInsight.init_from_file(filepath=tokenpath)
        assert isinstance(client, OTAInsight)
        assert client.token == 'testtokenvalue' 


@requests_mock.Mocker(kw='mock')
class TestGet:
    '''Test _get method of client'''

    def test_calls_get(self, client, **kwargs):
        '''test if it actually calls the requests get method'''
        client = client
        kwargs['mock'].get(client.url, json='passed')
        client._get()
        assert client.response == 'passed'

    def test_returns_dict(self, client, **kwargs):
        '''test if it returns json response parsed as dictionary'''
        client = client
        kwargs['mock'].get(client.url,
                           text='{"test_key": "test_value"}')
        client._get()
        assert isinstance(client.response, dict)
        assert client.response == {"test_key": "test_value"}


@requests_mock.Mocker(kw='mock')
class TestGetHotels:
    '''Test get wrapper for hotels endpoint'''

    def test_calls_correct_endpoint(self, client, **kwargs):
        '''Tests if it calls the correct endpoint - hotels'''
        client = client
        kwargs['mock'].get(f'{client.url}hotels',
                           text='{"hotels": "passed"}')
        assert client.get_hotels() == 'passed'


@requests_mock.Mocker(kw='mock')
class TestGetRates:
    '''Test get wrapper for rates endpoint'''

    def test_calls_correct_endpoint(self, client, **kwargs):
        '''Tests if it calls the correct endpoint - rates'''
        client = client
        kwargs['mock'].get(f'{client.url}rates',
                           text='{"rates": "passed"}')
        assert client.get_rates(555, '2020-01-01') == 'passed'
