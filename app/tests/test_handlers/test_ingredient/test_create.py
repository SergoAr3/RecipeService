import json

import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import Ingredient, Recipe, User
from app.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'recipe_data, ingredient_data, user_data',
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
                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(333),
                }
        )
    ]
)
async def test_create(client: TestClient, async_session_test, recipe_data, ingredient_data, user_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        await session.commit()
    resp = client.post("/ingredient", content=json.dumps(ingredient_data), headers=headers,
                       params={'recipe_id': recipe.id})
    assert resp.status_code == 204
    async with async_session_test() as session:
        ingredient = await session.execute(select(Ingredient).where(Ingredient.recipe_id == 1))
        ingredient = ingredient.scalar()
        await session.commit()
    assert ingredient.name == 'Помидоры'
    assert ingredient.quantity == '1кг.'
