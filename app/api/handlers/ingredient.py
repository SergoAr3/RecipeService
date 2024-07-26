from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

import app.api.errors as err
from app.auth.utils import get_current_active_auth_user
from app.schemas.ingredient import IngredientCreate, IngredientUpdate
from app.services.ingredient import IngredientService


ingredient_router = APIRouter(dependencies=[Depends(get_current_active_auth_user)])


@ingredient_router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_ingredient(
        ingredient: IngredientCreate,
        recipe_id: int,
        ingredient_service: Annotated[IngredientService, Depends()],
):
    try:
        await ingredient_service.create_ingredient(ingredient, recipe_id)
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@ingredient_router.delete('/{recipe_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(
        recipe_id: int,
        ingredient_name: str,
        ingredient_service: Annotated[IngredientService, Depends()],
):
    try:
        await ingredient_service.delete_ingredient(ingredient_name, recipe_id)
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@ingredient_router.patch('/{recipe_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_ingredient(
        ingredient: IngredientUpdate,
        recipe_id: int,
        ingredient_name: str,
        ingredient_service: Annotated[IngredientService, Depends()],
):
    try:
        await ingredient_service.update_ingredient(ingredient, recipe_id, ingredient_name)
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR
