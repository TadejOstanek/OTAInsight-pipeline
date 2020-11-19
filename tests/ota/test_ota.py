'''
Test OTAInsight API client
'''
from datetime import date
import os
import pytest
import requests
import requests_mock
from src.ota.ota import OTAInsight

@pytest.fixture(scope='module')
def init_client():
    '''Fixture to use the samle client and session
    for all tests'''
    return OTAInsight('test_token')


class TestInit:
    '''Test the __init__ constructor of the class'''

    def test_attributes(self):
        '''Make sure attributed are assigned correctly'''
        client = OTAInsight('test_token')
        assert client.token == 'test_token'
        assert client.url == 'https://api.otainsight.com/v2/'

    def test_raise_for_missing_token(self):
        '''Test if it raises an exception if token is not passed'''
        with pytest.raises(TypeError) as e:
            client = OTAInsight()

    def test_raise_for_wrong_type(self):
        '''Test if it raises an exception if token is not string'''
        with pytest.raises(TypeError) as e:
            client = OTAInsight(4543534534)
        with pytest.raises(TypeError) as e:
            client = OTAInsight(['fsd'])
            assert e.match('valid access token')

    def test_properties_read_only(self, init_client):
        '''test if session and token are read only properties'''
        with pytest.raises(AttributeError):
            init_client.token = 'new_token'
        with pytest.raises(AttributeError):
            init_client.session = requests.Session()


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
        client = OTAInsight.init_from_file(tokenpath)
        assert isinstance(client, OTAInsight)
        assert client.token == 'testtokenvalue' 


@requests_mock.Mocker(kw='mock')
class TestGet:
    '''Test _get method of client'''

    def test_calls_get(self, init_client, **kwargs):
        '''test if it actually calls the requests get method'''
        client = init_client
        kwargs['mock'].get(client.url, json='passed')
        client._get()
        assert client.response == 'passed'

    def test_returns_dict(self, init_client, **kwargs):
        '''test if it returns json response parsed as dictionary'''
        client = init_client
        kwargs['mock'].get(client.url,
                           text='{"test_key": "test_value"}')
        client._get()
        assert isinstance(client.response, dict)
        assert client.response == {"test_key": "test_value"}

    def test_uses_token(self, init_client, **kwargs):
        '''test if it uses token in the call'''
        client = init_client
        kwargs['mock'].get(
            f'{client.url}endpoint?token={client.token}',
            json='passed')
        client._get('endpoint')
        assert client.response == 'passed'


@requests_mock.Mocker(kw='mock')
class TestGetHotels:
    '''Test get wrapper for hotels endpoint'''

    def test_calls_correct_endpoint(self, init_client, **kwargs):
        '''Tests if it calls the correct endpoint - hotels'''
        client = init_client
        kwargs['mock'].get(f'{client.url}hotels',
                           text='{"hotels": "passed"}')
        assert client.get_hotels() == 'passed'


@requests_mock.Mocker(kw='mock')
class TestGetRates:
    '''Test get wrapper for rates endpoint'''

    def test_calls_correct_endpoint(self, init_client, **kwargs):
        '''Tests if it calls the correct endpoint - rates'''
        client = init_client
        kwargs['mock'].get(f'{client.url}rates',
                           text='{"rates": "passed"}')
        assert client.get_rates(555, '2020-01-01') == 'passed'
