from datetime import timedelta

import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.db import Recipe, Step, User
from app.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'recipe_data, step_data, user_data, query_params',
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
                    "hashed_password": bytes(333),
                },
                {
                    'step_number': 1
                }
        )
    ]
)
async def test_delete(client: TestClient, async_session_test, recipe_data, user_data, step_data, query_params):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    step = Step(**step_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        session.add(step)
        await session.commit()
    resp = client.delete(f"/step/{recipe.id}", headers=headers, params=query_params)
    assert resp.status_code == 204
    stmt = select(Step.id).where(Step.id == step.id)
    async with async_session_test() as session:
        step_id = await session.execute(stmt)
    step_id = step_id.scalar()
    assert step_id is None
