'''
test the combine data submodule
'''

from datetime import date, timedelta
import pytest
import pandas as pd
from src.data.combine import detect_required_files, combine_csvs

@pytest.fixture
def test_folder(tmpdir):
    '''generates test files in a temp folder'''
    files = [str(date.today()), str(date.today() - timedelta(days=2)),
             '2020-03-07', '2020-05-14', '2020-06-21', '2020-06-30',
             '2020-08-12', '2020-06-25', 'test_file']
    for file in files:
        pd.DataFrame([{'test': 0}]).to_csv(
            tmpdir.join(file), index=False)
    yield tmpdir

class TestDetectRequiredFiles:

    def test_last_week(self, test_folder):
        '''test if it returns files if they are from last week'''

        files_pass = detect_required_files(test_folder)
        assert str(date.today()) in files_pass
        assert str(date.today() - timedelta(days=2)) in files_pass

    def test_set_dates(self, test_folder):
        '''test if it keeps 4 special dates'''
        files_pass = detect_required_files(test_folder)
        req = set(['2020-03-07', '2020-05-14', 
                   '2020-06-21', '2020-06-30'])
        assert req.intersection(files_pass) == req

    def test_excludes_rest(self, test_folder):
        '''test if it excludes the past data'''
        exclude = set(['2020-08-12', '2020-06-25'])
        files_pass = detect_required_files(test_folder)
        assert exclude.intersection(files_pass) == set()

    def test_keeps_special(self, test_folder):
        '''test if it keeps special name files - without dates'''
        files_pass = detect_required_files(test_folder)
        assert 'test_file' in files_pass

class TestCombineCsvs:
    
    def test_integration(self, test_folder):
        result = combine_csvs(test_folder)
        req = pd.DataFrame([{'test': 0} for _ in range(7)])
        pd.testing.assert_frame_equal(result, req)