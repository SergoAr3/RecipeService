from fastapi import Depends

import app.api.errors as err
from app.repositories.ingredient import IngredientRepository
from app.repositories.recipe import RecipeRepository
from app.schemas.ingredient import (IngredientCreate, IngredientRead,
                                    IngredientUpdate,)


class IngredientService:
    def __init__(self,
                 ingredient_repository: IngredientRepository = Depends(),
                 recipe_repository: RecipeRepository = Depends()
                 ):
        self.ingredient_repository = ingredient_repository
        self.recipe_repository = recipe_repository

    async def get_by_ingredient_id(self, ingredient_id: int) -> IngredientRead:
        ingredient = await self.ingredient_repository.get(ingredient_id)
        ingredient = IngredientRead.from_orm(ingredient)
        return ingredient

    async def get_by_recipe_id(self, recipe_id: int) -> IngredientRead:
        ingredient = await self.ingredient_repository.get(recipe_id, by_recipe_id=True)
        ingredient = IngredientRead.from_orm(ingredient)
        return ingredient

    async def get_by_name(self, name: str) -> IngredientRead:
        ingredient = await self.ingredient_repository.get(name, by_name=True)
        ingredient = IngredientRead.from_orm(ingredient)
        return ingredient

    async def create_ingredient(self, ingredient: IngredientCreate, recipe_id: int) -> None:
        await self.ingredient_repository.create(ingredient, recipe_id)

    async def update_ingredient(self, ingredient: IngredientUpdate, recipe_id: int, ingredient_name: str):
        db_recipe = await self.recipe_repository.get(recipe_id)
        db_ingredient = await self.ingredient_repository.get(ingredient_name, by_name=True)
        if db_recipe and db_ingredient:
            ingredient_update_data = ingredient.model_dump(exclude_unset=True)
            await self.ingredient_repository.update(ingredient_update_data, recipe_id, ingredient_name)
        else:
            raise err.HTTP_404_NOT_FOUND_RECIPE_OR_INGREDIENT

    async def delete_ingredient(self, ingredient_name: str, recipe_id: int):
        await self.ingredient_repository.delete(ingredient_name, recipe_id)
