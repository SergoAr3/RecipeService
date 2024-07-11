import datetime
from typing import List

from fastapi import Depends

from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Recipe
from app.db.db import get_db
from app.schemas.recipe import RecipeCreate


class RecipeRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_last(self) -> Recipe:
        stmt = select(Recipe)
        res = await self.db.execute(stmt)
        recipes = res.scalar()
        return recipes

    async def get_all(self) -> List[Recipe]:
        stmt = select(Recipe)
        res = await self.db.execute(stmt)
        recipes = res.scalars().all()
        return recipes

    async def get(self, recipe_id: int = None, title: str = None, by_title: bool = False) -> Recipe:
        if by_title:
            stmt = select(Recipe).where(Recipe.title == title)
        else:
            stmt = select(Recipe).where(Recipe.id == recipe_id)
        res = await self.db.execute(stmt)
        recipe = res.scalar()
        return recipe

    async def get_time_filter(self, min_time: datetime.timedelta = None, max_time: datetime.timedelta = None) -> List[
        Recipe]:
        stmt = None
        if min_time and max_time:
            stmt = select(Recipe).where(min_time <= Recipe.total_time, Recipe.total_time <= max_time)
        elif min_time:
            stmt = select(Recipe).where(Recipe.total_time >= min_time)
        elif max_time:
            stmt = select(Recipe).where(Recipe.total_time <= max_time)
        res = await self.db.execute(stmt)
        recipe = res.scalars().all()
        return recipe

    async def get_sort_by_time(self, descending: bool = False) -> List[Recipe]:
        if descending:
            stmt = select(Recipe).order_by(desc(Recipe.total_time))
        else:
            stmt = select(Recipe).order_by(Recipe.total_time)
        res = await self.db.execute(stmt)
        recipe = res.scalars().all()
        return recipe

    async def get_rating_filter(self, min_rating: float = None, max_rating: float = None) -> List[Recipe]:
        stmt = None
        if min_rating and max_rating:
            stmt = select(Recipe).where(Recipe.average_rating >= min_rating, Recipe.average_rating <= max_rating)
        elif min_rating:
            stmt = select(Recipe).where(Recipe.average_rating >= min_rating)
        elif max_rating:
            stmt = select(Recipe).where(Recipe.average_rating <= max_rating)
        res = await self.db.execute(stmt)
        recipe = res.scalars().all()
        return recipe

    async def get_sort_by_average_rating(self, descending: bool = False) -> List[Recipe]:
        if descending:
            stmt = select(Recipe).order_by(desc(Recipe.average_rating))
        else:
            stmt = select(Recipe).order_by(Recipe.average_rating)
        res = await self.db.execute(stmt)
        recipe = res.scalars().all()
        return recipe

    async def create(self, recipe: RecipeCreate) -> Recipe:
        db_recipe = Recipe(
            title=recipe.title,
            description=recipe.description,
            total_time=sum([step.step_time for step in recipe.steps], datetime.timedelta(0))
        )
        self.db.add(db_recipe)
        return db_recipe

    async def delete(self, recipe: Recipe) -> None:
        await self.db.delete(recipe)

    async def update(self, recipe: RecipeCreate, recipe_id: int) -> None:
        await self.db.execute(update(Recipe).where(Recipe.id == recipe_id).values(title=recipe.title,
                                                                                  description=recipe.description,
                                                                                  total_time=sum(
                                                                                      step.step_time for step in
                                                                                      recipe.steps)))

    async def update_rating(self, recipe_title: str, rating: float):
        await self.db.execute(update(Recipe).where(Recipe.title == recipe_title).values(average_rating=rating))

    async def add_image(self, recipe_title: str, image_url: str) -> None:
        await self.db.execute(update(Recipe).where(Recipe.title == recipe_title).values(image_url=image_url))
