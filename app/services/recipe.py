import datetime
from typing import Literal

from fastapi import Depends

import app.api.errors as err
from app.db import Recipe
from app.repositories.ingredient import IngredientRepository
from app.repositories.rating import RatingRepository
from app.repositories.recipe import RecipeRepository
from app.repositories.step import StepRepository
from app.schemas.recipe import RecipeCreate, RecipeUpdate


class RecipeService:
    def __init__(self,
                 recipe_repository: RecipeRepository = Depends(),
                 ingredient_repository: IngredientRepository = Depends(),
                 step_repository: StepRepository = Depends(),
                 rating_repository: RatingRepository = Depends()
                 ):
        self.recipe_repository = recipe_repository
        self.ingredient_repository = ingredient_repository
        self.step_repository = step_repository
        self.rating_repository = rating_repository

    async def get_last_recipe(self) -> Recipe:
        recipe = await self.recipe_repository.get_last()
        return recipe

    async def get_recipe(self, recipe_id: int):
        recipe = await self.recipe_repository.get(recipe_id)
        average_rating = recipe.average_rating
        if not average_rating:
            average_rating = 'Оценок пока нет'
        recipe_data = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "total_time": recipe.total_time,
            "average_rating": average_rating,
            "image_id": recipe.image_id,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
        }
        return recipe_data

    async def get_recipes(self, recipes: list[Recipe] = None):
        if not recipes:
            recipes = await self.recipe_repository.get_all()
        res = []
        for recipe in recipes:
            average_rating = recipe.average_rating
            if not average_rating:
                average_rating = 'Оценок пока нет'
            recipe_data = {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "total_time": recipe.total_time,
                "average_rating": average_rating,
                "ingredients": recipe.ingredients,
                "steps": recipe.steps,
            }
            res.append(recipe_data)
        return res

    async def get_recipe_id_by_name(self, recipe_title: str):
        recipe_id = await self.recipe_repository.get_recipe_id(title=recipe_title)
        return recipe_id

    async def get_filtered_recipes(
            self,
            ingredient_name: str | None,
            min_time: datetime.timedelta | None,
            max_time: datetime.timedelta | None,
            max_rating: float | None,
            min_rating: float | None,
            sort_time: Literal['desc', 'asc'] | None,
            sort_rating: Literal['desc', 'asc'] | None
    ):
        recipes_id = None
        if ingredient_name:
            ingredients = await self.ingredient_repository.get(ingredient_name, by_name=True)
            if ingredients:
                recipes_id = [ingredient.recipe_id for ingredient in ingredients]
            else:
                return []

        filtered_recipes = await self.recipe_repository.get_filtered_recipes(
            max_time=max_time,
            min_time=min_time,
            max_rating=max_rating,
            min_rating=min_rating,
            sort_time=sort_time,
            sort_rating=sort_rating,
            recipes_id=recipes_id)
        recipes = await self.get_recipes(filtered_recipes)
        return recipes

    async def create_recipe_name(self, recipe: RecipeCreate) -> Recipe:
        db_recipe = await self.recipe_repository.create(recipe)
        if not db_recipe:
            raise err.HTTP_409_CONFLICT_CREATED
        return db_recipe

    async def create_recipe(self, recipe: RecipeCreate) -> None:
        db_recipe = await self.create_recipe_name(recipe)
        await self.get_last_recipe()
        ingredients = recipe.ingredients
        for ingredient in ingredients:
            await self.ingredient_repository.create(ingredient, db_recipe.id)
        steps = recipe.steps
        for step in steps:
            await self.step_repository.create(step, db_recipe.id)

    async def delete_recipe(self, recipe_id: int) -> Recipe:
        recipe = await self.recipe_repository.get(recipe_id)
        if recipe:
            await self.recipe_repository.delete(recipe)
            return recipe
        raise err.HTTP_404_NOT_FOUND_RECIPE

    async def update_recipe(self, recipe: RecipeUpdate, recipe_id: int) -> Recipe:
        db_recipe = await self.recipe_repository.get(recipe_id)

        if db_recipe:
            recipe_update_data = recipe.dict(exclude_unset=True)
            await self.recipe_repository.update(recipe_update_data, recipe_id)
            return db_recipe
        raise err.HTTP_404_NOT_FOUND_RECIPE

    async def add_image(self, image_id: str, recipe_title: str):
        recipe_update_data = {'image_id': image_id}
        await self.recipe_repository.update(recipe_update_data, recipe_title=recipe_title)
