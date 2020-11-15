# -*- coding: utf-8 -*-
"""
Helper functions that don't belong to a specific job/module
"""
from typing import List
from datetime import date


def generate_dates(base_date: date, 
                   start_month: int = 3) -> List[date]:
    '''Generate a list of starting dates 
    for each of which an export will be made

    The business logis is as following:
        In October and November generate reports for both years,
        the other months just for the current year, December only
        for the coming year. The starting date is always 1st of march

    Args:
        base_date(datetime.date): the base date for calculation
        start_month(int, optional): starting month for the returned
            dates

    Returns:
        list[datetime.date]

    Raises:
        TypeError: if input is not date type

    '''
    start_date = base_date.replace(month=start_month, day=1)
    start_date_next = start_date.replace(year=start_date.year + 1)
    sdates = [start_date, start_date_next]
    if base_date.month == 12:
        sdates.remove(start_date)
    elif base_date.month >= 10:
        pass
    else:
        sdates.remove(start_date_next)
    return sdates

