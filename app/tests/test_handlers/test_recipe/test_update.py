import json

import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import Recipe, User
from app.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'recipe_data, update_recipe_data_1, update_recipe_data_2, user_data',
    [
        (
                {
                    "id": 1,
                    "title": "Овощной салат",
                    "description": "Это легкое и освежающее блюдо, состоящее из свежих овощей",
                },
                {
                    "title": "Греческий салат",
                },
                {
                    "title": "Салат Цезарь",
                    "description": "Это салат цезарь",

                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(121241),
                }
        )
    ]
)
async def test_update(
        client: TestClient,
        async_session_test,
        recipe_data,
        update_recipe_data_1,
        update_recipe_data_2,
        user_data
):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        await session.commit()
    previous_description = recipe.description
    resp = client.patch(f"/recipe/{recipe.id}", content=json.dumps(update_recipe_data_1), headers=headers)
    assert resp.status_code == 204
    stmt = select(Recipe).where(Recipe.id == recipe.id)
    async with async_session_test() as session:
        recipe = await session.execute(stmt)
    recipe = recipe.scalar()
    assert recipe.title == update_recipe_data_1.get('title')
    assert recipe.description == previous_description
    resp = client.patch(f"/recipe/{recipe.id}", content=json.dumps(update_recipe_data_2), headers=headers,
                        params={'recipe_id': recipe.id})
    assert resp.status_code == 204
    stmt = select(Recipe).where(Recipe.id == recipe.id)
    async with async_session_test() as session:
        recipe = await session.execute(stmt)
    recipe = recipe.scalar()
    assert recipe.title == update_recipe_data_2.get('title')
    assert recipe.description == update_recipe_data_2.get('description')
