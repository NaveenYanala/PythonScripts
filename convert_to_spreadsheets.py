from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '11AaB1fq-9a7cp3s-vNMUrUi_DYTdOOptSSw8bZxAvTY'
sheet = service.spreadsheets()
data = [['nsharma51', "QUERY_SUBMITTED", "hive_20220919092832_e3db442f-5b01-4d7e-9625-c6ed59c01498",
         "cdo.soundbox_final_sales_olap_mtd_snapshot_v3,"
         "cdo_base.soundbox_final_sales_olap_mtd_snapshot_v3_20220919052210",
         "1900-01-01", "20220919", 1663579712462, 0, 0]]

res = sheet.values().append(spreadsheetId=spreadsheet_id,
                            range="Sheet1!a1:i1",
                            valueInputOption="USER_ENTERED",
                            insertDataOption="INSERT_ROWS",
                            body={"values":data}).execute()

print(res)
