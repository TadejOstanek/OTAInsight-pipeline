'''Test baseapi module'''

from datetime import date
import pytest
import requests
import requests_mock
from src.ota.baseapi import BaseAPI


@pytest.fixture(scope='module')
def init_client():
    '''Fixture to use the samle client and session
    for all tests'''
    return BaseAPI('https://testurl.com')


class TestBaseAPI:
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

    def test_max_retries(self, init_client):
        '''test if base class is set up with a max retry
        system
        '''
        client = init_client
        assert client.session.get_adapter(
            client.url).max_retries.total == 5


@requests_mock.Mocker(kw='mock')
class TestGet:
    '''test the get call'''

    def test_calls_get(self, init_client, **kwargs):
        '''test if it actually calls the requests get method'''
        client = init_client
        kwargs['mock'].get(client.url, text='passed')
        client._get()
        assert client.response.text == 'passed'

    @pytest.mark.parametrize('errors', [400, 404, 502])
    def test_raises_http_error(self, init_client, errors, **kwargs):
        '''it should raise an error when requests returns an error'''
        client = init_client
        kwargs['mock'].get(client.url, status_code=errors)
        with pytest.raises(requests.exceptions.HTTPError):
            client._get()

    def test_adds_endpoint(self, init_client, **kwargs):
        '''test if it correctly appends api endpoint to base url'''
        client = init_client
        kwargs['mock'].get(f'{client.url}endpoint',
                           text='passed')
        client._get('endpoint')
        assert client.response.text == 'passed'

    def test_uses_queryparams(self, init_client, **kwargs):
        '''does it sucessfully make a request with query params'''
        client = init_client
        kwargs['mock'].get(f'{client.url}endpoint?test=value',
                           text='passed')
        client._get('endpoint', test='value')
        assert client.response.text == 'passed'

    def test_parses_nonstring_qparams(self, init_client, **kwargs):
        '''does it sucessfully make a request with query params
        even if they are not a string'''
        client = init_client
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
