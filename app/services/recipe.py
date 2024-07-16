import datetime
from typing import List, Literal

from fastapi import Depends

import app.api.errors.level_400 as status_codes
from app.db import Recipe
from app.repositories.ingredient import IngredientRepository
from app.repositories.rating import RatingRepository
from app.repositories.recipe import RecipeRepository
from app.repositories.step import StepRepository
from app.schemas.recipe import RecipeCreate, RecipeRead


class RecipeService:
    def __init__(self, recipe_repository: RecipeRepository = Depends(),
                 ingredient_repository: IngredientRepository = Depends(),
                 step_repository: StepRepository = Depends(),
                 rating_repository: RatingRepository = Depends()):
        self.recipe_repository = recipe_repository
        self.ingredient_repository = ingredient_repository
        self.step_repository = step_repository
        self.rating_repository = rating_repository

    async def get_last_recipe(self) -> Recipe:
        recipe = await self.recipe_repository.get_last()
        return recipe

    async def get_recipe(self, recipe_id: int) -> RecipeRead:
        recipe = await self.recipe_repository.get(recipe_id)
        recipe_data = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "total_time": recipe.total_time,
            "average_rating": recipe.average_rating,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
        }
        recipe = RecipeRead.from_orm(recipe_data)
        return recipe

    @staticmethod
    async def get_recipes(recipes: list[Recipe]) -> list[str]:
        res = []
        for recipe in recipes:
            recipe_data = {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "total_time": recipe.total_time,
                "average_rating": recipe.average_rating,
                "ingredients": recipe.ingredients,
                "steps": recipe.steps,
            }
            res.append(str(RecipeRead.from_orm(recipe_data)))
        return res

    async def get_recipe_by_title(self, recipe_title: str) -> RecipeRead:
        recipe = await self.recipe_repository.get(title=recipe_title, by_title=True)
        recipe = await self.get_recipe(recipe.id)
        return recipe

    async def get_all_recipes(self) -> List[str]:
        db_recipes = await self.recipe_repository.get_all()
        recipes = await self.get_recipes(db_recipes)
        return recipes

    async def get_filtered_recipes(
            self,
            ingredient_name: str | None,
            min_time: datetime.timedelta | None,
            max_time: datetime.timedelta | None,
            max_rating: float | None,
            min_rating: float | None,
            sort_time: Literal['desc', 'asc'] | None,
            sort_rating: Literal['desc', 'asc'] | None
    ) -> list[str]:
        recipes_id = None
        if ingredient_name:
            ingredients = await self.ingredient_repository.get(ingredient_name, by_name=True)
            if ingredients:
                recipes_id = [ingredient.recipe_id for ingredient in ingredients]
            else:
                raise status_codes.HTTP_404_NOT_FOUND_ingredient

        filtered_recipes = await self.recipe_repository.get_filtered_recipes(
            ingredient_name=ingredient_name,
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
            raise status_codes.HTTP_409_CONFLICT_created
        return db_recipe

    async def create_recipe(self, recipe: RecipeCreate) -> None:
        db_recipe = await self.create_recipe_name(recipe)
        await self.get_last_recipe()
        for ingredient in recipe.ingredients:
            await self.ingredient_repository.create(ingredient, db_recipe.id)
        for step in recipe.steps:
            await self.step_repository.create(step, db_recipe.id)

    async def delete_recipe(self, recipe_id: int) -> Recipe:
        recipe = await self.recipe_repository.get(recipe_id)
        if recipe:
            await self.recipe_repository.delete(recipe)
            return recipe
        else:
            raise status_codes.HTTP_404_NOT_FOUND_recipe

    async def update_recipe(self, recipe: RecipeCreate, recipe_id: int) -> Recipe:
        db_recipe = await self.recipe_repository.get(recipe_id)
        if db_recipe:
            ingredients = recipe.ingredients
            for ingredient in ingredients:
                await self.ingredient_repository.update(ingredient, ingredient.name)
            steps = recipe.steps
            for step in steps:
                await self.step_repository.update(step, step.description)
            await self.recipe_repository.update(recipe, recipe_id)
        return db_recipe
