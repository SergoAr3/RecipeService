import datetime
from typing import List

from fastapi import Depends

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
        ingredients = await self.ingredient_repository.get(recipe_id, by_recipe_id=True)
        steps = await self.step_repository.get_all(recipe_id)
        recipe_data = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "total_time": recipe.total_time,
            "average_rating": recipe.average_rating,
            "ingredients": ingredients,
            "steps": steps,
            "image_url": recipe.image_url
        }
        recipe = RecipeRead.from_orm(recipe_data)
        return recipe

    async def get_recipe_by_title(self, recipe_title: str) -> RecipeRead:
        recipe = await self.recipe_repository.get(title=recipe_title, by_title=True)
        ingredients = await self.ingredient_repository.get(recipe.id, by_recipe_id=True)
        steps = await self.step_repository.get_all(recipe.id)
        recipe_data = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "total_time": recipe.total_time,
            "average_rating": recipe.average_rating,
            "ingredients": ingredients,
            "steps": steps,
            "image_url": recipe.image_url
        }
        recipe = RecipeRead.from_orm(recipe_data)
        return recipe

    async def get_all_recipes(self) -> List[str]:
        db_recipes = await self.recipe_repository.get_all()
        recipes = []
        for recipe in db_recipes:
            ingredients = await self.ingredient_repository.get(recipe.id, by_recipe_id=True)
            steps = await self.step_repository.get_all(recipe.id)
            recipe_data = {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "total_time": recipe.total_time,
                "average_rating": recipe.average_rating,
                "ingredients": ingredients,
                "steps": steps,
                "image_url": recipe.image_url
            }
            recipes.append(str(RecipeRead.from_orm(recipe_data)))
        return recipes

    async def get_by_ingredient(self, ingredient_name: str) -> List[str]:
        ingredients = await self.ingredient_repository.get(ingredient_name, by_name=True)
        recipes = []
        for ingredient in ingredients:
            recipe = await self.recipe_repository.get(ingredient.recipe_id)
            recipe_ingredients = await self.ingredient_repository.get(ingredient.recipe_id, by_recipe_id=True)
            recipe_steps = await self.step_repository.get_all(ingredient.recipe_id)
            recipe_data = {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "total_time": recipe.total_time,
                "average_rating": recipe.average_rating,
                "ingredients": recipe_ingredients,
                "steps": recipe_steps,
                "image_url": recipe.image_url
            }
            recipes.append(str(RecipeRead.from_orm(recipe_data)))
        return recipes

    async def get_by_total_time(self, min_time: datetime.timedelta = None, max_time: datetime.timedelta = None,
                                sort_by_time: bool = False,
                                descending: bool = False):
        recipes = []
        db_recipes = []
        if min_time and max_time:
            db_recipes = await self.recipe_repository.get_time_filter(min_time=min_time, max_time=max_time)
        elif min_time:
            db_recipes = await self.recipe_repository.get_time_filter(min_time=min_time)
        elif max_time:
            db_recipes = await self.recipe_repository.get_time_filter(max_time=max_time)
        elif sort_by_time:
            if descending:
                db_recipes = await self.recipe_repository.get_sort_by_time(descending=True)
            else:
                db_recipes = await self.recipe_repository.get_sort_by_time()

        for db_recipe in db_recipes:
            recipe_ingredients = await self.ingredient_repository.get(db_recipe.id, by_recipe_id=True)
            recipe_steps = await self.step_repository.get_all(db_recipe.id)
            recipe_data = {
                "id": db_recipe.id,
                "title": db_recipe.title,
                "description": db_recipe.description,
                "total_time": db_recipe.total_time,
                "average_rating": db_recipe.average_rating,
                "ingredients": recipe_ingredients,
                "steps": recipe_steps,
                "image_url": db_recipe.image_url

            }
            recipes.append(str(RecipeRead.from_orm(recipe_data)))
        if not recipes:
            return 'No recipes found'
        return recipes

    async def get_by_average_rating(self, min_rating: float = None, max_rating: float = None,
                                    sort_by_rating: bool = False,
                                    descending: bool = False):
        recipes = []
        db_recipes = []
        if min_rating and max_rating:
            db_recipes = await self.recipe_repository.get_rating_filter(min_rating=min_rating, max_rating=max_rating)
        elif min_rating:
            db_recipes = await self.recipe_repository.get_rating_filter(min_rating=min_rating)
        elif max_rating:
            db_recipes = await self.recipe_repository.get_rating_filter(max_rating=max_rating)
        elif sort_by_rating:
            if descending:
                db_recipes = await self.recipe_repository.get_sort_by_average_rating(descending=True)
            else:
                db_recipes = await self.recipe_repository.get_sort_by_average_rating()

        for db_recipe in db_recipes:
            recipe_ingredients = await self.ingredient_repository.get(db_recipe.id, by_recipe_id=True)
            recipe_steps = await self.step_repository.get_all(db_recipe.id)
            recipe_data = {
                "id": db_recipe.id,
                "title": db_recipe.title,
                "description": db_recipe.description,
                "total_time": db_recipe.total_time,
                "average_rating": db_recipe.average_rating,
                "ingredients": recipe_ingredients,
                "steps": recipe_steps,
                "image_url": db_recipe.image_url

            }
            recipes.append(str(RecipeRead.from_orm(recipe_data)))

        return recipes

    async def create_recipe_name(self, recipe: RecipeCreate) -> Recipe:
        db_recipe = await self.recipe_repository.create(recipe)
        return db_recipe

    async def create_recipe(self, recipe: RecipeCreate) -> None:
        db_recipe = await self.create_recipe_name(recipe)
        await self.get_last_recipe()
        for ingredient in recipe.ingredients:
            await self.ingredient_repository.create(ingredient, db_recipe.id)
        for step in recipe.steps:
            await self.step_repository.create(step, db_recipe.id)

    async def delete_recipe(self, recipe_id: int) -> None:
        recipe = await self.recipe_repository.get(recipe_id)
        if recipe:
            await self.recipe_repository.delete(recipe)

    async def update_recipe(self, recipe: RecipeCreate, recipe_id: int) -> None:
        db_recipe = await self.recipe_repository.get(recipe_id)
        if db_recipe:
            ingredients = recipe.ingredients
            for ingredient in ingredients:
                await self.ingredient_repository.update(ingredient, ingredient.name)
            steps = recipe.steps
            for step in steps:
                await self.step_repository.update(step, recipe_id, step.description)
            await self.recipe_repository.update(recipe, recipe_id)

    async def add_image(self, recipe_title: str, image_url: str):
        await self.recipe_repository.add_image(recipe_title, image_url)

    # async def update_rating(self, recipe_id: int) -> float:
    #     ratings = await self.rating_repository.get(recipe_id, by_recipe_id=True)
    #     total = 0
    #     count = 0
    #     for rating in ratings:
    #         total += rating.rating
    #     return total / count
