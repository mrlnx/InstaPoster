from __future__ import print_function
import pickle
import os.path
from datetime import datetime
import io

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

class DriveApi:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive.readonly']
        self.id = '1Ur0Qn_H_tGi00mVPUmn-Z-u0gKN_CmpX3FXH1CWJXOo'
        self.files = None

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token_drive.pickle'):
            with open('./token_drive.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './credentials_drive.json', self.scopes)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('./token_drive.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

        self.set_files()

    def set_files(self, directory_id=None):
        q = []
        params = {}

        q.append("'%s' in parents" % '1THPa-z7FBgecZlxkxeR5MDoKnO-0Czhm')

        params['q'] = ' and '.join(q)

        # Call the Drive v3 API
        results = self.service.files().list(**params).execute()

        self.files = results.get('files', [])

    def download(self, filename, username):

        print(self.files)

        if not self.files:
            print('No files found.')
        else:

            for file in self.files:

                drive_filename =  file['name'].split('.')

                print(filename, drive_filename[0:1])

                if file['name'] == filename:

                    request = self.service.files().get_media(fileId=file['id'])
                    fh = io.FileIO('./public/%s/images/%s' % (username, file['name']), 'wb')

                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        #print("Download %s " % str(int(status.progress() * 100)))
                    else:
                        return './public/%s/images/%s' % (username, file['name']);
        return False
