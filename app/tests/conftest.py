import asyncio
import os
import shutil
from typing import Any, Generator, Mapping

import pytest
from dotenv import load_dotenv
from googleapiclient.http import MediaFileUpload
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.sql import text
from starlette.testclient import TestClient

from app.auth.utils import encode_jwt
from app.db.db import get_db
from app.repositories.google_drive.config import get_gd
from app.repositories.google_drive.google_drive import GoogleDriveRepository
from main import app


load_dotenv()

CLEAN_TABLES = [
    'user',
    'recipe',
    'ingredient',
    'step',
    'rating',
    'image_recipe',
    'image_step',

]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test() -> async_sessionmaker:
    engine = create_async_engine(os.getenv('TEST_DATABASE_URL'), future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"""TRUNCATE TABLE "{table_for_cleaning}" CASCADE;"""))

    drive_service = await get_gd()
    files_id = drive_service.files().list(
        pageSize=10,
        fields="nextPageToken, files(id)",
        q=f"'{os.getenv('TEST_GD_FOLDER_ID')}' in parents").execute()

    for file in files_id['files']:
        file_id = file['id']
        drive_service.files().delete(fileId=file_id).execute()


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            os.getenv('TEST_DATABASE_URL'), future=True,
        )

        # create session for the interaction with database
        test_async_session = async_sessionmaker(
            test_engine, expire_on_commit=False
        )
        async with test_async_session() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as e:
                logger.error(e)
                await session.rollback()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[GoogleDriveRepository] = TestGoogleDriveRepository
    with TestClient(app) as client:
        yield client


async def create_test_auth_headers_for_user(username: str) -> Mapping[str, str]:
    jwt_payload = {
        'sub': username,
        'username': username,
    }
    token = await encode_jwt(jwt_payload)
    return {"Authorization": f"Bearer {token}"}


class TestGoogleDriveRepository(GoogleDriveRepository):

    def upload_image(self, file) -> str:
        filename = file.filename
        temp_file_path = f'/tmp/{filename}'
        with open(temp_file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        media = MediaFileUpload(temp_file_path, resumable=True)
        file_metadata = {
            'name': filename,
            'parents': [os.getenv('TEST_GD_FOLDER_ID')]
        }
        file_id = self.gd.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return file_id['id']
