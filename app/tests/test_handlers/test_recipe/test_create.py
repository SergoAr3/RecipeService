import json
from datetime import timedelta

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
                    "ingredients": [
                        {
                            "name": "Помидоры",
                            "quantity": "1кг."
                        }
                    ],
                    "steps": [
                        {
                            "number": 1,
                            "description": "Порезать мелко овощи",
                            "step_time": "00:10:00"
                        }
                    ]
                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(333),
                }
        )
    ]
)
async def test_create(client: TestClient, async_session_test, recipe_data, user_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    async with async_session_test() as session:
        session.add(user)
        await session.commit()
    resp = client.post("/recipe", content=json.dumps(recipe_data), headers=headers)
    assert resp.status_code == 204
    recipe_title = recipe_data.get('title')
    async with async_session_test() as session:
        recipe = await session.execute(select(Recipe).where(Recipe.title == recipe_title))
        recipe = recipe.scalar()
        await session.commit()
    step = recipe.steps[0]
    ingredient = recipe.ingredients[0]
    assert recipe.title == "Овощной салат"
    assert recipe.description == "Это легкое и освежающее блюдо, состоящее из свежих овощей"
    assert step.description == "Порезать мелко овощи"
    assert step.step_time == timedelta(minutes=10)
    assert ingredient.name == 'Помидоры'
    assert ingredient.quantity == '1кг.'
