import io
from os import getenv
from dotenv import load_dotenv
from fastapi import Depends

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from app.repositories.google_drive.config import get_gd

load_dotenv()


class GoogleDriveRepository:
    def __init__(self, gd: build = Depends(get_gd)):
        self.gd = gd

    def upload_image(self, image_name: str, image_path) -> str:
        media = MediaFileUpload(image_path, resumable=True)
        file_metadata = {
            'name': image_name,
            'parents': [getenv('GD_FOLDER_ID')]
        }
        file_id = self.gd.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return file_id['id']

    def download_image(self, image_id: str, recipe_title: str) -> None:
        image = self.gd.files().get_media(fileId=image_id)
        with io.FileIO(f'{recipe_title}.jpg', 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, image)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
