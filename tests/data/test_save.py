'''
Test save data submodule
'''

import os
from pathlib import Path
from datetime import date
import pytest
import pandas as pd
from pytest_mock import mocker
from src.data.save import save_export, prepare_paths


@pytest.fixture
def data():
    '''Loads api data for function tests'''
    path = Path(
        __file__).parents[0] / 'mock_data/prepared_data.csv'
    yield pd.read_csv(path)

class TestPreparePaths:
    '''Test function that prepares the path where results are saved'''

    def test_return(self):
        rpath = prepare_paths(2020, 'TestHotel', 'data_export', 
            'ratesResult')
        tpath = Path() / ('2020/data_export/TestHotel/'
            'ratesResult.csv')
        assert rpath == tpath


class TestSaveExport:

    def test_creates_directory(self, data, mocker, tmpdir):
        '''test if function creates a directory if it doesn't exist'''
        # mock prepare paths so it retuns a non-existing path
        mocker.patch('src.data.save.prepare_paths', 
            lambda x, y, z, a, b: Path(tmpdir.join(
                'subfolder/test_file.csv')))
        mocker.patch.object(pd.DataFrame, 'to_csv')
        folder_name = save_export(
            data, 2019, 'TestHotel', 'test_folder', 'test_file')
        assert os.path.isdir(tmpdir / 'subfolder')
        # test if it returns the path to results
        assert folder_name == tmpdir / 'subfolder'