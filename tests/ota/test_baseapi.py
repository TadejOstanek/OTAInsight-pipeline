'''Test baseapi module'''

from datetime import date
import os
import pytest
import requests
import requests_mock
from src.ota.baseapi import BaseAPI, TokenAPI


@pytest.fixture(scope='module')
def client():
    '''Fixture to use the samle client and session
    for all tests'''
    return BaseAPI('https://testurl.com')

@pytest.fixture(scope='module')
def token_client():
    '''Fixture to use the samle client and session
    for all tests'''
    return TokenAPI('https://testurl.com', 'test_token')


class TestBaseAPI:

    class TestInit:
        '''test the init constructor'''
        def test_attributes(self):
            '''Make sure attributed are assigned correctly'''
            client = BaseAPI('https://testurl.com')
            assert client.url == 'https://testurl.com'
            assert isinstance(client.session, requests.Session)
            assert client.response is None

        def test_read_only(self):
            '''test attributes that should be read only'''
            client = BaseAPI('https://testurl.com')
            with pytest.raises(AttributeError):
                client.url = 'b'
            with pytest.raises(AttributeError):
                client.session = 'b'

        def test_max_retries(self, client):
            '''test if base class is set up with a max retry
            system
            '''
            assert client.session.get_adapter(
                client.url).max_retries.total == 5


    @requests_mock.Mocker(kw='mock')
    class TestGet:
        '''test the get call'''

        def test_calls_get(self, client, **kwargs):
            '''test if it actually calls the requests get method'''
            kwargs['mock'].get(client.url, text='passed')
            client._get()
            assert client.response.text == 'passed'

        @pytest.mark.parametrize('errors', [400, 404, 502])
        def test_raises_http_error(self, client, errors, **kwargs):
            '''it should raise an error when requests returns an error'''
            kwargs['mock'].get(client.url, status_code=errors)
            with pytest.raises(requests.exceptions.HTTPError):
                client._get()

        def test_adds_endpoint(self, client, **kwargs):
            '''test if it correctly appends api endpoint to base url'''
            kwargs['mock'].get(f'{client.url}endpoint',
                               text='passed')
            client._get('endpoint')
            assert client.response.text == 'passed'

        def test_uses_queryparams(self, client, **kwargs):
            '''does it sucessfully make a request with query params'''
            kwargs['mock'].get(f'{client.url}endpoint?test=value',
                               text='passed')
            client._get('endpoint', test='value')
            assert client.response.text == 'passed'

        def test_parses_nonstring_qparams(self, client, **kwargs):
            '''does it sucessfully make a request with query params
            even if they are not a string'''
            kwargs['mock'].get(
                f'{client.url}endpoint?test_int=9',
                text='passed')
            kwargs['mock'].get(
                f'{client.url}endpoint?test_date=2020-05-01',
                text='passed')
            client._get('endpoint', test_int=9)
            assert client.response.text == 'passed'
            client._get('endpoint', test_date=date(2020, 5, 1))
            assert client.response.text == 'passed'


class TestTokenAPI:
    '''test tokenapi subclass'''
    class TestInit:

        def test_implements_base_class(self, token_client):
            '''should implement BaseAPI'''
            assert isinstance(token_client, BaseAPI)
            assert TokenAPI(url='', token='').url == ''

        def test_token(self, token_client):
            '''Make sure attributed are assigned correctly'''
            assert token_client.token == 'test_token'

        def test_token_read_only(self, token_client):
            '''Make sure attributed are assigned correctly'''
            with pytest.raises(AttributeError):
                token_client.token = 'new_token'

        def test_raise_for_wrong_type(self):
            '''Test if it raises an exception if token is not string'''
            with pytest.raises(TypeError) as e:
                client = TokenAPI(4543534534)
            with pytest.raises(TypeError) as e:
                client = TokenAPI(['fsd'])
                assert e.match('valid access token')


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
            client = TokenAPI.init_from_file(tokenpath,
                url='testurl')
            assert isinstance(client, TokenAPI)
            assert client.token == 'testtokenvalue' 

    class TestGet:
        '''tests the extension of _get by TokenAPI'''
        @requests_mock.Mocker(kw='mock')
        def test_uses_token(self, token_client, **kwargs):
            '''test if it uses token in the call'''
            client = token_client
            kwargs['mock'].get(
                f'{client.url}endpoint?token={client.token}',
                text='passed')
            client._get('endpoint')
            assert client.response.text == 'passed'
