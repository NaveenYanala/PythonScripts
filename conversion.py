import os
from googleapiclient.http import MediaFileUpload
from Google import Create_Service

CLIENT_SECRET_FILE = 'Client_Secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_VERSION, API_NAME, SCOPES)


def convert_to_excel(file_path: str, folder_ids: str):
    if not os.path.exists(file_path):
        print(f'{file_path} not found')
        return
    try:
        print('naveen')
        file_metadata = {
            'name': os.path.splitext(os.path.basename(file_path))[0],
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': folder_ids
        }
        media = MediaFileUpload(
            filename=file_path,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response = service.files().create(
            media_body=media,
            body=file_metadata
        ).execute()
        print('naveen')
        print(response)
        return response

    except Exception as e:
        print(e)
        return


convert_to_excel('/Users/yanalanaveenreddy/desktop/HiveAnalysis/hive.xlsx', '1l2rDs6kVuASfEB5Q8yWtHWvYIgOgA9Ve')
