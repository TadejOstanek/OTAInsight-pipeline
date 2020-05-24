# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:46:16 2020

@author: tadej
"""
from ota import OTAInsight
from datetime import date
import pandas as pd
from pathlib import Path
import numpy as np

kiani_subid = 89365

date_stamp = date.today()

with open(Path('auth/ota_token.txt'), 'r') as fa:
    token = fa.read()

client = OTAInsight(token)

plist = dict()
for site in ['bookingdotcom', 'expedia']:
    plist[site] = client.get_rates(
        sub_id=str(kiani_subid), los='3', ota=site,
        from_date='2020-03-01', shop_length='250')

rates_data = pd.concat(plist).reset_index().rename(
    columns={'level_0': 'site'}).drop(columns='level_1')
rates_data['date_stamp'] = str(date_stamp)

rates_data = rates_data.loc[:, ['date_stamp', 'site', 'arrivalDate',
                                'hotelName', 'value']]

rates_data = rates_data.assign(value=rates_data.value.replace(0, np.nan))

rates_data.to_csv('data_export/rates_result' + str(date_stamp) + '.csv',
                  index=False)
