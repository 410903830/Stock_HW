#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:24:26 2024

@author: zhangjunzhi


#####Google Driver ######

"""


from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'axial-trail-422616-i8-fd32f2e56319.json'
PARENT_FOLDER_ID = "1JtR_Af85FrKzZbZVSo-oHVF-KX_IU4-D"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE , scopes=SCOPES)
    return creds



#上傳至google drive
def upload_file(file_path, Name):
    creds= authenticate()
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        
        'name' : f"{Name}",
        'parents' : [PARENT_FOLDER_ID]
        
        }
    file = service.files().create(
        body = file_metadata,
        media_body = file_path
        ).execute()
    






