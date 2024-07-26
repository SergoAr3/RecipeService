import json
from datetime import timedelta

import pytest
from starlette.testclient import TestClient

from app.db import Ingredient, Recipe, Step


@pytest.mark.parametrize(
    'recipe_data, ingredients_data, step_data',
    [
        (

                {
                    'id': 1,
                    "title": "Овощной салат",
                    "description": "Это легкое и освежающее блюдо, состоящее из свежих овощей",
                },

                {
                    "name": "Помидоры",
                    "quantity": "1кг.",
                    'recipe_id': 1
                },

                {
                    "number": 1,
                    "description": "Порезать мелко овощи",
                    "step_time": timedelta(minutes=10),
                    'recipe_id': 1
                }

        )

    ]
)
async def test_get_recipe(client: TestClient, async_session_test, recipe_data, step_data, ingredients_data):
    recipe = Recipe(**recipe_data)
    step = Step(**step_data)
    ingredient = Ingredient(**ingredients_data)
    async with async_session_test() as session:
        session.add(recipe)
        session.add(step)
        session.add(ingredient)
        await session.commit()
    resp = client.get(f"/recipe/{recipe.id}")
    resp_content = json.loads(resp.content.decode("utf-8"))
    assert resp.status_code == 200
    assert resp_content['recipe'].get('steps') == [{
        'id': step.id,
        "description": "Порезать мелко овощи",
        'image_id': None,
        'recipe_id': 1,
        "number": 1,
        "step_time": 600.0,

    }]
    assert resp_content['recipe'].get('ingredients') == [
        {'name': 'Помидоры', 'quantity': '1кг.', 'id': ingredient.id, 'recipe_id': 1}]


@pytest.mark.parametrize(
    'recipes_data',
    [

        [

            {
                'id': 1,
                "title": "Овощной салат",
                "description": "Это легкое и освежающее блюдо, состоящее из свежих овощей",
            },

            {
                'id': 2,
                "title": "Пицца",
                "description": "Пицца описание",
            },

            {
                'id': 3,
                "title": "Котлеты",
                "description": "Котлеты описание",

            }
        ]

    ]
)
async def test_get_all_recipes(client: TestClient, async_session_test, recipes_data):
    for recipe_data in recipes_data:
        recipe = Recipe(**recipe_data)
        async with async_session_test() as session:
            session.add(recipe)
            await session.commit()
    resp = client.get("/recipe/all")
    resp_content = json.loads(resp.content.decode("utf-8"))
    assert resp.status_code == 200
    assert resp_content.get('recipes')[0]['title'] == 'Овощной салат'
    assert resp_content.get('recipes')[1]['title'] == 'Пицца'
    assert resp_content.get('recipes')[2]['title'] == 'Котлеты'
