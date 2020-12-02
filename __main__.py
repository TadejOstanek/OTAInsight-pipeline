# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 12:50:42 2020
Get data from api and create all_data result files
@author: tadej
"""

import logging
from datetime import date
from src.ota import OTAInsight
import src.helpers.helpers as helpers
from src.data import prepare, save, combine


logger = logging.getLogger(__name__)


def main():
    """
    Runs the pipeline from OTA-Insight to locally saved data
    Returns:
        list[pathlib.Path]: list of folders where final results
        were saved
    """
    date_stamp = date.today()
    client = OTAInsight()
    # get hotels to iterate over
    hotels = client.get_hotels()
    # get list of starting dates to iterate over
    start_dates = helpers.generate_dates(date_stamp)
    folders = []
    for start_date in start_dates:
        for hotel in hotels:
            hotel_name = hotel['name']
            pdict = dict()
            for site in ['bookingdotcom', 'expedia']:
                pdict[site] = client.get_rates(
                    sub_id=hotel['subscription_id'], from_date=start_date,
                    los='2', ota=site, shop_length='250')
            rates_data = prepare.prep_data(pdict, date_stamp)
            folder = save.save_export(
                rates_data, year=start_date.year, hotel=hotel_name,
                foldername='data_export',
                filename=f'rates_result{date_stamp}',
                gzip=True)
            combined = combine.combine_csvs(folder)
            folder = save.save_export(
                combined, year=start_date.year, hotel=hotel_name,
                filename='all_data', foldername='results')
            folders.append(folder)
    return folders


if __name__ == '__main__':
    logger.info('Process started')
    main()
    logger.info('Process finished')
