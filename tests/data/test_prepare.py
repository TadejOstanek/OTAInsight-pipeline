'''
Test prepare data submodule
'''

from pathlib import Path
import json
import pytest
import pandas as pd
from src.data.prepare import concat_dict_to_pd

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