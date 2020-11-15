'''
Test OTAInsight API client
'''
from datetime import date
import os
import pytest
import requests
import requests_mock
from src.ota.ota import OTAInsight, query_params_to_str

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
        assert OTAInsight.URL == 'https://api.otainsight.com/v2/'
        assert isinstance(client.session, requests.Session)
        assert client.response is None

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


class TestAppendToken:
    '''test method that appeds token to dictionary
    of query parameters'''

    def test_returns_dict_with_token(self, init_client):
        '''test if it returns a dictionary with token key if
        no additional are passed'''
        client = init_client
        qparams = client._append_token({})
        assert isinstance(qparams, dict)
        assert 'token' in qparams

    def test_returns_correct_token(self, init_client):
        '''test if it assigns the correct token'''

        client = init_client
        qparams = client._append_token({})
        assert qparams == {'token': client.token}

    def test_combine_with_other_params(self, init_client):
        '''test if it combines other passed query parameters 
        into one dictionary'''
        client = init_client
        qparams = client._append_token({'folder': 'hotels'})
        assert qparams == {'token': client.token,
                           'folder': 'hotels'}

    def test_raise_ifnot_dict(self, init_client):
        '''should raise a attribute error if dictionary is not passed'''
        with pytest.raises(TypeError):
            init_client._append_token('wrong_argument')


@requests_mock.Mocker(kw='mock')
class TestGet:
    '''Test _get method of client'''

    def test_calls_get(self, init_client, **kwargs):
        '''test if it actually calls the requests get method'''
        client = init_client
        kwargs['mock'].get(OTAInsight.URL, json='passed')
        client._get()
        assert client.response == 'passed'

    def test_returns_dict(self, init_client, **kwargs):
        '''test if it returns json response parsed as dictionary'''
        client = init_client
        kwargs['mock'].get(OTAInsight.URL,
                           text='{"test_key": "test_value"}')
        client._get()
        assert isinstance(client.response, dict)
        assert client.response == {"test_key": "test_value"}

    @pytest.mark.parametrize('errors', [400, 404, 502])
    def test_raises_http_error(self, init_client, errors, **kwargs):
        '''it should raise an error when requests returns an error'''
        client = init_client
        kwargs['mock'].get(OTAInsight.URL, status_code=errors)
        with pytest.raises(requests.exceptions.HTTPError):
            client._get()

    def test_adds_endpoint(self, init_client, **kwargs):
        '''test if it correctly appends api endpoint to base url'''
        client = init_client
        kwargs['mock'].get(f'{OTAInsight.URL}endpoint',
                           json='passed')
        client._get('endpoint')
        assert client.response == 'passed'

    def test_uses_queryparams(self, init_client, **kwargs):
        '''does it sucessfully make a request with query params'''
        client = init_client
        kwargs['mock'].get(f'{OTAInsight.URL}endpoint?test=value',
                           json='passed')
        client._get('endpoint', test='value')
        assert client.response == 'passed'

    def test_parses_nonstring_qparams(self, init_client, **kwargs):
        '''does it sucessfully make a request with query params
        even if they are not a string'''
        client = init_client
        kwargs['mock'].get(
            f'{OTAInsight.URL}endpoint?test_int=9',
            json='passed')
        kwargs['mock'].get(
            f'{OTAInsight.URL}endpoint?test_date=2020-05-01',
            json='passed')
        client._get('endpoint', test_int=9)
        assert client.response == 'passed'
        client._get('endpoint', test_date=date(2020, 5, 1))
        assert client.response == 'passed'

    def test_uses_token(self, init_client, **kwargs):
        '''test if it uses token in the call'''
        client = init_client
        kwargs['mock'].get(
            f'{OTAInsight.URL}endpoint?token={client.token}',
            json='passed')
        client._get('endpoint')
        assert client.response == 'passed'


@requests_mock.Mocker(kw='mock')
class TestGetHotels:
    '''Test get wrapper for hotels endpoint'''

    def test_calls_correct_endpoint(self, init_client, **kwargs):
        '''Tests if it calls the correct endpoint - hotels'''
        client = init_client
        kwargs['mock'].get(f'{OTAInsight.URL}hotels',
                           text='{"hotels": "passed"}')
        assert client.get_hotels() == 'passed'


@requests_mock.Mocker(kw='mock')
class TestGetRates:
    '''Test get wrapper for rates endpoint'''

    def test_calls_correct_endpoint(self, init_client, **kwargs):
        '''Tests if it calls the correct endpoint - rates'''
        client = init_client
        kwargs['mock'].get(f'{OTAInsight.URL}rates',
                           text='{"rates": "passed"}')
        assert client.get_rates(555, '2020-01-01') == 'passed'


class TestQueryParamsToStr:
    '''Test if function correctly turns query dictionary
    values to strings'''

    def test_empty_dict(self):
        '''test if on empty it returns empty'''
        assert isinstance(
            query_params_to_str({}), dict)

    def test_on_string(self):
        '''on string should return as is'''
        assert query_params_to_str(
            {'test': 'test'}) == {'test': 'test'}

    def test_on_int(self):
        '''it should pass integers'''
        assert query_params_to_str(
            {'test': 111}) == {'test': '111'}

    def test_on_date(self):
        '''it should parse dates'''
        assert query_params_to_str(
            {'test': date(2020, 1, 1)}) == {'test': '2020-01-01'}

    def test_on_float(self):
        '''it should raise error on floats'''
        with pytest.raises(TypeError):
            query_params_to_str(
                {'test': 23.5})

    def test_multiple_ok(self):
        '''it should handle multiple entries'''
        assert query_params_to_str(
            {'test_date': date(2020, 5, 1),
             'test_int': 531,
             'test_str': 'str'}) == {'test_date': '2020-05-01',
                                     'test_int': '531',
                                     'test_str': 'str'}