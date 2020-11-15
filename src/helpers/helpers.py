# -*- coding: utf-8 -*-
"""
Helper functions that don't belong to a specific job/module
"""
from typing import List
from datetime import date


def generate_dates(base_date: date) -> List[date]:
    '''Generate a list of starting dates
    for each of which an export will be made

    The business logis is as following:
        In October and November generate reports for both years,
        the other months just for the current year, December only
        for the coming year

    Args:
        base_date(datetime.date)

    Returns:
        list[datetime.date]

    Raises:
        TypeError: if input is not date type

    '''
    start_date = base_date.replace(month=3, day=1)
    start_date_next = start_date.replace(year=start_date.year + 1)

    if base_date.month == 12:
        sdates = [start_date_next]
    elif base_date.month >= 10:
        sdates = [start_date, start_date_next]
    else:
        sdates = [start_date]
    return sdates
