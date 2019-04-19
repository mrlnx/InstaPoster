from __future__ import print_function
import pickle
import os.path
from datetime import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class SheetsApi:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.spreadsheet_id = '1Ur0Qn_H_tGi00mVPUmn-Z-u0gKN_CmpX3FXH1CWJXOo'
        self.range_name = 'Posts!A:H'
        self.values = None

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('./token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './credentials.json', self.scopes)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('./token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

        self.set_values()

    def set_values(self):

        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    range=self.range_name).execute()
        values = result.get('values', [])

        if not values:
            self.values = None
        else:
            self.values = values

    def get_values_by_datetime(self):

        now = datetime.now()
        current_datetime = datetime(now.year, now.month, now.day, now.hour, now.minute, 0)

        new_values = []

        if len(self.values) > 0:
            column_names = self.values[0]
            
            for value in self.values[1:]:

                datetime_obj = datetime.strptime('%s %s' % (value[1], value[2]), '%d-%m-%Y %H:%M')

                if datetime_obj == current_datetime:

                    value_obj = {}

                    for c in range(len(column_names)):
                        value_obj[column_names[c]] = value[c]

                    new_values.append(value_obj)

        return new_values
