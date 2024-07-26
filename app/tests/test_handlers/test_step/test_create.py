import json
from datetime import timedelta

import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import Recipe, Step, User
from app.tests.conftest import create_test_auth_headers_for_user


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
                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(333),
                }
        )
    ]
)
async def test_create(client: TestClient, async_session_test, recipe_data, step_data, user_data):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        await session.commit()
    step_data['step_time'] = f'{timedelta(minutes=10)}'
    resp = client.post("/step", content=json.dumps(step_data), headers=headers, params={'recipe_id': recipe.id})
    assert resp.status_code == 204
    async with async_session_test() as session:
        step = await session.execute(select(Step).where(Step.recipe_id == 1))
        step = step.scalar()
        await session.commit()
    assert step.description == 'Порезать мелко овощи'
    assert step.step_time == timedelta(minutes=10)
