from os import getenv
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()


class GoogleDriveService:
    def __init__(self, gd: build):
        self.gd = gd

    def upload_image(self, image_name: str, image_path) -> str:
        media = MediaFileUpload(image_path, resumable=True)
        file_metadata = {
            'name': image_name,
            'parents': [getenv('GD_FOLDER_ID')]
        }
        file_id = self.gd.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return file_id['id']
