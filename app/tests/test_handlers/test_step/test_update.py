import json
from datetime import timedelta

import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import Recipe, Step, User
from app.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'recipe_data, step_data, update_step_data, user_data, query_params',
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
                    "number": 1,
                    "description": "Порезать крупно овощи",
                    "step_time": timedelta(minutes=10),
                    "recipe_id": 1

                },
                {
                    "username": "Sergo",
                    "hashed_password": bytes(333),
                },
                {
                    'step_number': 1
                }
        )
    ]
)
async def test_update(client: TestClient, async_session_test, recipe_data, step_data, user_data, update_step_data,
                      query_params):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    step = Step(**step_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        session.add(step)
        await session.commit()
    update_step_data['step_time'] = f'{timedelta(minutes=20)}'
    resp = client.patch(f"/step/{recipe.id}", content=json.dumps(update_step_data), headers=headers,
                        params=query_params)
    assert resp.status_code == 204
    async with async_session_test() as session:
        step = await session.execute(select(Step).where(Step.recipe_id == 1))
        step = step.scalar()
        await session.commit()
    assert step.description == 'Порезать крупно овощи'
    assert step.step_time == timedelta(minutes=20)
