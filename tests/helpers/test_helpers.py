'''
Test helpers module
'''

from datetime import date
import pytest
from src.helpers.helpers import generate_dates


class TestGenerateDates(object):
    '''Test function that generates a list of starting dates'''

    def test_input_control(self):
        '''should return an error if datetime.date is not passed'''
        with pytest.raises(TypeError):
            generate_dates('2020-02-01')

    def test_start_month(self):
        '''the dates in return should first of the starting month'''
        result = generate_dates(date(2020, 5, 15))
        assert result == [date(2020, 3, 1)]

    @pytest.mark.parametrize('month', [10, 11])
    def test_double_months(self, month):
        '''for october and november should return 2 dates'''
        test_date = date(2015, month, 7)
        result = generate_dates(test_date)
        assert len(result) == 2
        assert result == [date(2015, 3, 1), date(2016, 3, 1)]

    def test_december(self):
        '''for december should return only the next year'''
        result = generate_dates(date(1999, 12, 31))
        assert result == [date(2000, 3, 1)]
