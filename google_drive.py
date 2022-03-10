# -*- coding: utf-8 -*-
"""
Created on Sun May  3 15:29:52 2020
connect to google drive
@author: tadej
"""
from datetime import date
import json
from src.helpers.helpers import generate_dates
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
date_stamp = date.today()


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



report_dates = generate_dates(date_stamp)

with open("config/google_drive_folders.json") as json_file:
    config = json.load(json_file)

for report_date in report_dates:
    year_config = config[str(report_date.year)]

    for hotel, folder_data in year_config.items():

        overwrite_upload(folder_data["results"], 'all_data.csv',
                         path=f'{report_date.year}/results/{hotel}')

        overwrite_upload(folder_data["data_export"],
                         'rates_result' + str(date.today()) + '.csv.gz',
                         path=f'{report_date.year}/data_export/{hotel}')
