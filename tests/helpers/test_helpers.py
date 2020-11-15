'''
Test helpers module
'''

from datetime import date
import pytest
from src import helpers


class TestGenerateDates(object):
    '''Test function that generates a list of starting dates'''

    def test_input_control(self):
        '''should return an error if datetime.date is not passed'''
        with pytest.raises(TypeError):
            helpers.generate_dates('2020-02-01')

    def test_output_control(self):
        '''should return a list of dates'''
        result = helpers.generate_dates(date(2020, 1, 1))
        assert isinstance(result, list)
        assert isinstance(result[0], date)

    def test_start_month(self):
        '''the dates in return should first of the starting month'''
        result = helpers.generate_dates(date(2020, 5, 15), 
            start_month=3)
        assert result == [date(2020, 3, 1)]

    @pytest.mark.parametrize('month', [10, 11])
    def test_double_months(self, month):
        '''for october and november should return 2 dates'''
        test_date = date(2015, month, 7)
        result = helpers.generate_dates(test_date, start_month=4)
        assert len(result) == 2
        assert result == [date(2015, 4, 1), date(2016, 4, 1)]

    def test_december(self):
        '''for december should return only the next year'''
        result = helpers.generate_dates(date(1999, 12, 31), 
            start_month=1)
        assert result == [date(2000, 1, 1)]
