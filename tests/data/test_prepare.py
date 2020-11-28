'''
Test prepare data submodule
'''

from pathlib import Path
import json
from datetime import date
import pytest
import pandas as pd
from src.data.prepare import concat_dict_to_pd, prep_data

@pytest.fixture
def api_data():
    '''Loads api data for function tests'''
    path = Path(
        __file__).parents[0] / 'mock_data/mock_api_result.json'
    with open(path, 'r') as file:
        yield json.load(file)

class TestConcatDictToPd:

    def test_converts_to_df(self, api_data):
        '''test if it returns a data frame'''
        assert isinstance(concat_dict_to_pd(api_data), pd.DataFrame)

    def test_contains_site(self, api_data):
        '''test if the resulting DataFrame contains a site column
        with correct values'''
        result = concat_dict_to_pd(api_data)
        # if column is present
        assert 'site' in list(result)
        assert set(result.site) == set(['expedia', 'bookingdotcom'])

class TestPrepData:
    '''Integration preparation data'''

    def test_date_col(self, api_data):
        '''test if it correctly assignts date column'''
        result = prep_data(api_data, date.today())
        assert (result.date_stamp == date.today()).all()

    def test_columns(self, api_data):
        '''test if it returns selected columns'''
        assert set(['date_stamp', 'site', 'arrivalDate', 
            'hotelName', 'value']) == set(
            prep_data(api_data, date.today()))

    def test_zero_replacement(self, api_data):
        '''test if it replaces 0 values with nan'''
        result = prep_data(api_data, date.today())
        assert result.value.isna().any()
        assert not (result.value == 0).any()

    def test_full_integration(self, api_data):
        result = prep_data(api_data, date(2020, 1, 1))
        path = Path(__file__).parents[0] / 'mock_data/prepared_data.csv'
        test = pd.read_csv(path, parse_dates=['date_stamp'])
        test.loc[:, 'date_stamp'] = test.date_stamp.dt.date
        pd.testing.assert_frame_equal(result, test)

