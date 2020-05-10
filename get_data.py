# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:46:16 2020

@author: tadej
"""
from ota import OTAInsight
from datetime import date

kiani_subid = 89365

date_stamp = date.today()

with open('auth/ota_token.txt', 'r') as fa:
    token = fa.read()

client = OTAInsight(token)

rates_data = client.get_rates(sub_id=str(kiani_subid), los='3',
                              from_date='2020-03-01', shop_length='250')

rates_data['date_stamp'] = date_stamp

rates_data = rates_data.loc[:, ['date_stamp', 'arrivalDate', 'hotelName',
                            'value']]

rates_data.to_csv('data_export/rates_result' + str(date_stamp) + '.csv',
                  index=False)
