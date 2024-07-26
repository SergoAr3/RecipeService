import pytest
from sqlalchemy import and_, select
from starlette.testclient import TestClient

from app.db import Rating, Recipe, User
from app.tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    'recipe_data, user_data, rating',
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
                    "rating": 5
                }
        )
    ]
)
async def test_rate(client: TestClient, async_session_test, recipe_data, user_data, rating):
    headers = await create_test_auth_headers_for_user(user_data['username'])
    user = User(**user_data)
    recipe = Recipe(**recipe_data)
    async with async_session_test() as session:
        session.add(user)
        session.add(recipe)
        await session.commit()
    resp = client.put(f"/recipe/rate/{recipe.title}", params=rating, headers=headers)
    assert resp.status_code == 204
    get_average_rating = select(Recipe.average_rating).where(Recipe.id == recipe.id)
    get_rating = select(Rating).where(and_(Rating.recipe_id == recipe.id, Rating.user_id == user.id))
    async with async_session_test() as session:
        average_rating = await session.execute(get_average_rating)
        average_rating = average_rating.scalar()
        rating = await session.execute(get_rating)
        rating = rating.scalar()
        await session.commit()
    assert average_rating == 5
    assert rating.rating == 5
    assert rating.user_id == user.id
    assert rating.recipe_id == recipe.id
