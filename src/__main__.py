# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 12:50:42 2020
Get data from api and create all_data result files
@author: tadej
"""

import logging
import logging.config
from pathlib import Path
from datetime import date
import yaml
from src.ota.ota import OTAInsight
from src import data, helpers

logging.config.dictConfig(yaml.load(open('logs/config.yaml'),
                                    Loader=yaml.FullLoader))
logger = logging.getLogger(__name__)


def main():
    date_stamp = date.today()

    client = OTAInsight.init_from_file('auth/ota_token.txt')
    hotels = client.get_hotels()
    start_dates = helpers.generate_dates(date_stamp)

    for sdate in start_dates:
        for hotel in hotels:
            hname = hotel['name']
            plist = dict()
            for site in ['bookingdotcom', 'expedia']:
                plist[site] = client.get_rates(
                    sub_id=str(hotel['subscription_id']), los='2', ota=site,
                    from_date=str(sdate), shop_length='250')
            rates_data = helpers.prep_data(plist, date_stamp)
            folder = helpers.save_export(rates_data, str(sdate.year), hname,
                                         f'rates_result{str(date_stamp)}',
                                         'data_export', compression='gzip')
            combined = helpers.combine_csvs(folder)

            helpers.save_export(combined, str(sdate.year), hname,
                                'all_data', 'results')


if __name__ == '__main__':
    logger.info('Process started')
    main()
    logger.info('Process finished')
