import os
from datetime import timedelta

import pytest
from dotenv import load_dotenv
from googleapiclient.http import MediaFileUpload
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import ImageStep, Recipe, Step, User
from app.repositories.google_drive.config import get_gd
from app.tests.conftest import create_test_auth_headers_for_user


load_dotenv()


@pytest.mark.parametrize(
    'recipe_data, step_data, user_data',
    [
        (
                {
                    'id': 1,
                    "title": "Овощной салат",
                    "description": "Это легкое и освежающее блюдо, состоящее из свежих овощей",
                },
                {
                    "number": 1,
                    "description": "Порезать мелко овощи",
                    "step_time": timedelta(minutes=10),
                    "recipe_id": 1
                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(121241),
                }
        )
    ]
)
async def test_upload_step_image(client: TestClient, async_session_test, recipe_data, step_data, user_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    step = Step(**step_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        session.add(step)
        await session.commit()
    with open('../../test_images/p_O.jpg', 'rb') as file:
        resp = client.post("/step/image",
                           headers=headers,
                           params={'recipe_title': recipe.title, 'step_number': step.number},
                           files={'file': ("p_O.jpg", file, "image/jpg")})
    assert resp.status_code == 204
    get_image = select(ImageStep)
    get_step_image_id = select(Step.image_id)
    async with async_session_test() as session:
        image = await session.execute(get_image)
        step_image_id = await session.execute(get_step_image_id)
    image = image.scalar()
    step_image_id = step_image_id.scalar()
    assert image.step_id == step.id
    assert step_image_id == image.id


@pytest.mark.parametrize(
    'recipe_data, step_data, user_data, step_image_data',
    [
        (
                {
                    "id": 1,
                    "title": "Овощной салат",
                    "description": "Это легкое и освежающее блюдо, состоящее из свежих овощей",
                },
                {
                    "id": 1,
                    "number": 1,
                    "description": "Порезать мелко овощи",
                    "step_time": timedelta(minutes=10),
                    "recipe_id": 1
                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(121241),
                },
                {
                    "id": '',
                    "url": '',
                    "step_id": 1
                }
        )
    ]
)
async def test_get_step_image(client: TestClient, async_session_test, recipe_data, user_data, step_data,
                              step_image_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    drive_service = await get_gd()

    media = MediaFileUpload('../../test_images/p_O.jpg', resumable=True)
    file_metadata = {
        'name': 'p_O.jpg',
        'parents': [os.getenv('TEST_GD_FOLDER_ID')]
    }
    image = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    image_id = image['id']
    image_url = f'https://drive.google.com/uc?id={image_id}'
    step_image_data['id'] = image_id
    step_image_data['url'] = image_url
    step_data['image_id'] = image_id

    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    step = Step(**step_data)
    step_image = ImageStep(**step_image_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        session.add(step)
        session.add(step_image)
        await session.commit()

    resp = client.get(f"/step/image/{recipe.title}/{step.number}", headers=headers)
    assert resp.status_code == 200
    assert resp.headers['content-type'] == 'image/jpeg'
