# -*- coding: utf-8 -*-
"""
Created on Sun May  3 15:29:52 2020
connect to google drive
@author: tadej
"""

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
f = drive.CreateFile({'parents': [{'id': '1niAms7QddkNxn8NU3b6AKHViA-efVJfa'}]})
f.SetContentFile('all_data.csv')
f.Upload() # Upload the file.

