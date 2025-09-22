import os
import io
import re
import time
from tqdm import tqdm
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

class GoogleDriveDownloader:
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    def __init__(self, credentials_file='credentials.json',
                 token_file='token.pickle',
                 download_dir='downloads'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)
        self.service = self.authenticate()

    def authenticate(self):
        creds = None
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        return build('drive', 'v3', credentials=creds)

    def extract_id(self, link_or_id: str) -> str:
        """
        Extracts a Google Drive file/folder ID from:
        - File links (/d/<ID>)
        - Folder links (/folders/<ID>)
        - Query params (?id=<ID>)
        - Raw IDs
        Returns the best guess ID.
        """
        text = link_or_id.strip()

        # Common patterns first
        patterns = [
            r"/d/([a-zA-Z0-9_-]{20,})",       # File link
            r"/folders/([a-zA-Z0-9_-]{20,})", # Folder link
            r"[?&]id=([a-zA-Z0-9_-]{20,})"    # Query param
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return m.group(1)

        # Fallback: any long token (Drive IDs are usually 20+ chars)
        m = re.search(r"[a-zA-Z0-9_-]{20,}", text)
        return m.group(0) if m else text

    def is_folder(self, file_id):
        meta = self.service.files().get(fileId=file_id,
                                        fields='mimeType').execute()
        return meta['mimeType'] == 'application/vnd.google-apps.folder'

    def get_file_metadata(self, file_id):
        return self.service.files().get(
            fileId=file_id,
            fields="name, mimeType, size"
        ).execute()

    def list_folder(self, folder_id):
        files = []
        page_token = None
        while True:
            response = self.service.files().list(
                q=f"'{folder_id}' in parents and trashed=false",
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, size)',
                pageToken=page_token
            ).execute()
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files

    def get_unique_filename(self, path):
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = path
        while os.path.exists(new_path):
            new_path = f"{base}_{counter}{ext}"
            counter += 1
        return new_path

    def download_file(self, file_id, file_name, dest_folder):
        dest_path = os.path.join(dest_folder, file_name)
        dest_path = self.get_unique_filename(dest_path)

        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(dest_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        print(f"⬇️ Downloading: {dest_path}")
        pbar = tqdm(total=100, unit='%')
        while not done:
            status, done = downloader.next_chunk()
            if status:
                pbar.n = int(status.progress() * 100)
                pbar.refresh()
        pbar.close()

    def download_folder(self, folder_id, dest_folder):
        os.makedirs(dest_folder, exist_ok=True)
        items = self.list_folder(folder_id)
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                self.download_folder(item['id'],
                                     os.path.join(dest_folder, item['name']))
            else:
                self.download_file(item['id'], item['name'], dest_folder)

    def download(self, link_or_id):
        file_id = self.extract_id(link_or_id)
        meta = self.get_file_metadata(file_id)
        if self.is_folder(file_id):
            target_dir = os.path.join(self.download_dir, meta['name'])
            self.download_folder(file_id, target_dir)
        else:
            self.download_file(file_id, meta['name'], self.download_dir)
        print("✅ Download complete!")

if __name__ == "__main__":
    downloader = GoogleDriveDownloader()
    link = input("Enter Google Drive file/folder link or ID: ").strip()
    downloader.download(link)
