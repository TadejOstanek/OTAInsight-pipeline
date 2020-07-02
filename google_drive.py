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


# kiani results
overwrite_upload('1Y-bjMHHzllC9Q3GNK_IYHKp5bQVf2Nem', 'all_data.csv',
                 path='results/Kiani Beach Resort Family All Inclusive')
# kalyves results
overwrite_upload('1xnzukMUCq8GcYlGQ0u5o0tcqbGc3J2Qq', 'all_data.csv',
                 path='results/Kalyves Beach Hotel')
# kiani beach daily
overwrite_upload('1eDqBlFCu1lroPyh4dQPx7mYyxOIWreDa',
                 'rates_result' + str(date.today()) + '.csv',
                 path='data_export/Kiani Beach Resort Family All Inclusive')
# kalyves daily
overwrite_upload('1I5HB8w_fON6qas2G-CTG3Rwx7iqJq-iR',
                 'rates_result' + str(date.today()) + '.csv',
                 path='data_export/Kalyves Beach Hotel')
