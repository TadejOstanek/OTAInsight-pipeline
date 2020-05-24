# -*- coding: utf-8 -*-
"""
Created on Sun May  3 15:29:52 2020
connect to google drive
@author: tadej
"""
from datetime import date
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# upload all data

f = drive.CreateFile({
    'parents': [{'id': '1niAms7QddkNxn8NU3b6AKHViA-efVJfa'}]})
f.SetContentFile('all_data.csv')
f.Upload() # Upload the file.

# upload the raw file
f = drive.CreateFile({
    'parents': [{'id': '131uqtvxWy0qIzg4Fs0wIszeM09B7ZJ07'}]})
f.SetContentFile('data_export/rates_result' + str(date.today()) + '.csv')
f.Upload() # Upload the file.
rates_data.to_csv('data_export/rates_result' + str(date_stamp) + '.csv')