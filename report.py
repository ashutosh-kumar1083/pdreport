import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] 

SPREADSHEETID = '1bkTINLcAD8e1qgtz_bibdPqt93i9KaW2OcotAOIFKxE'


def main():
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('pdalertclient.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    try:
        sheets = build('sheets', 'v4', credentials=credentials).spreadsheets()
        #sheets = service.spreadsheets()

        result =  sheets.values().get(spreadsheetId=SPREADSHEETID, range='Sheet1!A1:D7').execute()
        values = result.get('values', [])

        for row in values:
            print(row)

    except HttpError as error:
        print(error)

if __name__ == '__main__':
    main()