import os
import io
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Google Drive API credentials
CLIENT_ID = r'C:\Users\yashv\Downloads\client_secret_51487583740-9jn81d4oeulbvd169uqhggjcdecmq0ba.apps.googleusercontent.com.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Authentication
creds = None
token_path = 'token.json'
if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_ID, SCOPES)
        creds = flow.run_local_server(port=0)
    with open(token_path, 'w') as token:
        token.write(creds.to_json())

# Google Drive service
drive_service = build('drive', 'v3', credentials=creds)

# Search for WhatsApp backup files
query = "mimeType='application/octet-stream' and name contains 'msgstore.db.crypt'"
results = drive_service.files().list(q=query).execute()
files = results.get('files', [])

# Download the first file (assuming there is one)
if files:
    file_id = files[0]['id']
    try:
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO('downloaded_backup.db.crypt', 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download Status: {status.progress() * 100:.2f}%")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        fh.close()

print("Download Complete!")