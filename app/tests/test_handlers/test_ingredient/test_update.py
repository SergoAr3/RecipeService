import json

import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import Ingredient, Recipe, User
from app.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'recipe_data, ingredient_data, update_ingredient_data, user_data, query_params',
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
                    "name": 'Огурцы',
                    "quantity": "0.5 кг.",
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
async def test_update(client: TestClient, async_session_test, recipe_data, ingredient_data, user_data,
                      update_ingredient_data, query_params):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    ingredient = Ingredient(**ingredient_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        session.add(ingredient)
        await session.commit()
    resp = client.patch(f"/ingredient/{recipe.id}", content=json.dumps(update_ingredient_data), headers=headers,
                        params=query_params)
    assert resp.status_code == 204
    async with async_session_test() as session:
        ingredient = await session.execute(select(Ingredient).where(ingredient.recipe_id == 1))
        ingredient = ingredient.scalar()
        await session.commit()
    assert ingredient.name == 'Огурцы'
    assert ingredient.quantity == '0.5 кг.'
