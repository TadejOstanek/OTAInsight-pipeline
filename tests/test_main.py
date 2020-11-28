'''
end-to-end tests
'''
from datetime import date
import json
import pytest
from pathlib import Path
import pandas as pd
from pytest_mock import mocker
from src.ota import OTAInsight
from src.data import save
from src import __main__

def mock_get_hotels(self):
    '''mock so it returns two fake hotels with min req info'''
    return [{'name': 'Hotel1', 'subscription_id': 4328},
            {'name': 'Hotel2', 'subscription_id': 4528}]

def mock_get_rates(self, sub_id, from_date, los, ota, shop_length):
    '''mock so it doesn't connect to api but returns premade data'''
    with open(
        'tests/data/mock_data/mock_api_result.json', 'r') as file:
            data = json.load(file)
    # the prepared data has an entry for booking and one for expedia
    return data[ota]

def outer_mock(temp):
    # in order to pass tmp_path fixture you have to play with nested
    # functions, as the inner function cannot accept extra arguments
    # as it is used for mocking
    def mock_prepare_paths(year, hotel, foldername, 
        filename, gzip=False):
        extension = '.csv.gz' if gzip else '.csv'
        return (temp / str(year) / foldername / hotel /
                (filename + extension))
    return mock_prepare_paths


def test_end_to_end(mocker, tmp_path):
    '''full end to end test'''
    mocker.patch.object(OTAInsight, 'get_hotels', mock_get_hotels)
    mocker.patch.object(OTAInsight, 'get_rates', mock_get_rates)
    mocker.patch('src.data.save.prepare_paths', 
        new=outer_mock(tmp_path))
    # this writes the files, captures the multiple folders where 
    # data was written to, but use only the first, as in this test
    # they all contain the same data
    folder = __main__.main()[0]
    print(folder)
    written_final = pd.read_csv(folder / 'all_data.csv')
    inter_file = folder.parents[1] / 'data_export'/ 'Hotel1'
    written_interm = pd.read_csv(
        inter_file / f'rates_result{str(date.today())}.csv.gz')
    test = pd.read_csv('tests/data/mock_data/prepared_data.csv')
    # this is hard coded for now in the other
    test.loc[:, 'date_stamp'] = str(date.today())
    # intermediate and final are the same as there are no past files
    pd.testing.assert_frame_equal(written_final, test)
    pd.testing.assert_frame_equal(written_interm, test)
    