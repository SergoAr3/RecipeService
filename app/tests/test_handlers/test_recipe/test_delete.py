import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import Recipe, User
from app.tests.conftest import create_test_auth_headers_for_user


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
async def test_delete(client: TestClient, async_session_test, recipe_data, user_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        await session.commit()
    resp = client.delete(f"/recipe/{recipe.id}", headers=headers)
    assert resp.status_code == 204
    stmt = select(Recipe.id).where(Recipe.id == recipe.id)
    async with async_session_test() as session:
        recipe_id = await session.execute(stmt)
    recipe_id = recipe_id.scalar()
    assert recipe_id is None
