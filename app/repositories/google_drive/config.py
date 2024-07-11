from os import getenv
from dotenv import load_dotenv

from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()


async def get_gd() -> build:
    credentials = service_account.Credentials.from_service_account_file(
        getenv('SERVICE_ACCOUNT_FILE'), scopes=[getenv('SCOPE')])

    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service
