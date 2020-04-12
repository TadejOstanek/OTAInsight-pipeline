# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:46:16 2020

@author: tadej
"""
from ota import OTAInsight

kiani_subid = 89365

with open('auth/token.txt', 'r') as f:
    token = f.read()

client = OTAInsight(token)

rates_data = client.get_rates(sub_id=str(kiani_subid), los='3',
                         from_date='2020-03-01', shop_length='250')

rates_data.to_csv('rates_result.csv', index=False)
