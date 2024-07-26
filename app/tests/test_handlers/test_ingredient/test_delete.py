import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import Ingredient, Recipe, User
from app.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'recipe_data, ingredient_data, user_data, query_params',
    [
        (
                {
                    'id': 1,
                    "title": "Овощной салат",
                    "description": "Это легкое и освежающее блюдо, состоящее из свежих овощей",
                },
                {
                    "name": 'Помидоры',
                    "quantity": "1кг.",
                    "recipe_id": 1
                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(333),
                },
                {
                    'ingredient_name': 'Помидоры'
                }
        )
    ]
)
async def test_delete(client: TestClient, async_session_test, recipe_data, user_data, ingredient_data, query_params):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    ingredient = Ingredient(**ingredient_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        session.add(ingredient)
        await session.commit()
    resp = client.delete(f"/ingredient/{recipe.id}", headers=headers, params=query_params)
    assert resp.status_code == 204
    stmt = select(Ingredient.id).where(Ingredient.id == ingredient.id)
    async with async_session_test() as session:
        ingredient_id = await session.execute(stmt)
    ingredient_id = ingredient_id.scalar()
    assert ingredient_id is None
