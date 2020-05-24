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

def overwrite_upload(folderid, file_name, path=None):
    file_list = drive.ListFile(
        {'q': f"'{folderid}' in parents and trashed = False"}).GetList()
    for file in file_list:
        if file['title'] == file_name:
            file.Delete()
    f = drive.CreateFile({'parents': [{'id': folderid}],
                          'title': file_name})
    if path is not None:
        file_path = path + '/' + file_name
    else:
        file_path = file_name
    f.SetContentFile(file_path)
    f.Upload()

overwrite_upload('1niAms7QddkNxn8NU3b6AKHViA-efVJfa', 'all_data.csv')
overwrite_upload('131uqtvxWy0qIzg4Fs0wIszeM09B7ZJ07',
                 'rates_result' + str(date.today()) + '.csv',
                 path='data_export')
