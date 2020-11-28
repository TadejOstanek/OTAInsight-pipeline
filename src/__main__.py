# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 12:50:42 2020
Get data from api and create all_data result files
@author: tadej
"""

import logging
from datetime import date
from src.ota import OTAInsight
import helpers
from data import prepare, save, combine


logger = logging.getLogger(__name__)


def main():
    date_stamp = date.today()
    client = OTAInsight.init_from_file('config/auth/ota_token.txt')
    # get hotels to iterate over
    hotels = client.get_hotels()
    # get list of starting dates to iterate over
    start_dates = helpers.generate_dates(date_stamp)

    for sdate in start_dates:
        for hotel in hotels:
            hname = hotel['name']
            pdict = dict()
            for site in ['bookingdotcom', 'expedia']:
                pdict[site] = client.get_rates(
                    sub_id=str(hotel['subscription_id']), los='2', ota=site,
                    from_date=str(sdate), shop_length='250')
            rates_data = prepare.prep_data(pdict, date_stamp)
            folder = save.save_export(
                rates_data, str(sdate.year), hname,
                f'rates_result{str(date_stamp)}',
                'data_export', compression='gzip')
            combined = combine.combine_csvs(folder)

            save.save_export(combined, str(sdate.year), hname,
                             'all_data', 'results')


if __name__ == '__main__':
    logger.info('Process started')
    main()
    logger.info('Process finished')
