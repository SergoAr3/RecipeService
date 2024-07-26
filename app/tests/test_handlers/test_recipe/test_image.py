import os

import pytest
from dotenv import load_dotenv
from googleapiclient.http import MediaFileUpload
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import ImageRecipe, Recipe, User
from app.repositories.google_drive.config import get_gd
from app.tests.conftest import create_test_auth_headers_for_user


load_dotenv()


@pytest.mark.parametrize(
    'recipe_data, user_data',
    [
        (
                {
                    "title": "Овощной салат",
                    "description": "Это легкое и освежающее блюдо, состоящее из свежих овощей",
                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(121241),
                }
        )
    ]
)
async def test_upload_recipe_image(client: TestClient, async_session_test, recipe_data, user_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        await session.commit()
    with open('../../test_images/p_O.jpg', 'rb') as file:
        resp = client.post("/recipe/image", headers=headers, params={'recipe_title': recipe.title},
                           files={'file': ("p_O.jpg", file, "image/jpg")})
    assert resp.status_code == 204
    get_recipe_image_id = select(Recipe.image_id).where(Recipe.id == recipe.id)
    get_image_id = select(ImageRecipe.id)
    async with async_session_test() as session:
        recipe_image_id = await session.execute(get_recipe_image_id)
        image_id = await session.execute(get_image_id)
    recipe_image_id = recipe_image_id.scalar()
    image_id = image_id.scalar()
    assert image_id == recipe_image_id
    assert recipe_image_id is not None


@pytest.mark.parametrize(
    'recipe_data, user_data, recipe_image_data',
    [
        (
                {
                    "title": "Овощной салат",
                    "description": "Это легкое и освежающее блюдо, состоящее из свежих овощей",
                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(121241),
                },
                {
                    "id": '',
                    "url": ''
                }
        )
    ]
)
async def test_get_recipe_image(client: TestClient, async_session_test, recipe_data, user_data, recipe_image_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    drive_service = await get_gd()

    media = MediaFileUpload(
        '../../test_images/p_O.jpg',
        resumable=True)
    file_metadata = {
        'name': 'p_O.jpg',
        'parents': [os.getenv('TEST_GD_FOLDER_ID')]
    }
    image = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    image_id = image['id']
    image_url = f'https://drive.google.com/uc?id={image_id}'
    recipe_image_data['id'] = image_id
    recipe_image_data['url'] = image_url
    recipe_data['image_id'] = image_id

    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    recipe_image = ImageRecipe(**recipe_image_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        session.add(recipe_image)
        await session.commit()

    resp = client.get(f"/recipe/image/{recipe.title}", headers=headers)
    assert resp.status_code == 200
    assert resp.headers['content-type'] == 'image/jpeg'
