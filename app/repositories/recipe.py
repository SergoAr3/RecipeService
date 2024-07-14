import datetime
from typing import List

from fastapi import Depends

from sqlalchemy import select, update, desc, or_
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

    async def get_filtered_recipes(
            self,
            ingredient_name: str | None = None,
            recipes_id: list[Recipe] = None,
            min_time: datetime.timedelta | None = None,
            max_time: datetime.timedelta | None = None,
            max_rating: float | None = None,
            min_rating: float | None = None,
            sort_time: str | None = None,
            sort_rating: str | None = None
    ) -> list[Recipe]:
        stmt = select(Recipe)
        if ingredient_name:
            conditions = []
            for recipe_id in recipes_id:
                conditions.append(Recipe.id == recipe_id)
            stmt = stmt.where(or_(*conditions))
        if min_time and max_time:
            stmt = stmt.where(Recipe.total_time >= min_time, Recipe.total_time <= max_time)
        elif min_time:
            stmt = stmt.where(Recipe.total_time >= min_time)
        elif max_time:
            stmt = stmt.where(Recipe.total_time <= max_time)
        if min_rating and max_rating:
            stmt = stmt.where(Recipe.average_rating >= min_rating, Recipe.average_rating <= max_rating)
        elif min_rating:
            stmt = stmt.where(Recipe.average_rating >= min_rating)
        elif max_rating:
            stmt = stmt.where(Recipe.average_rating <= max_rating)
        if sort_time:
            if sort_time == 'desc':
                stmt = stmt.order_by(desc(Recipe.total_time))
            elif sort_time == 'asc':
                stmt = stmt.order_by(Recipe.total_time)
        if sort_rating:
            if sort_rating == 'desc':
                stmt = stmt.order_by(desc(Recipe.average_rating))
            elif sort_rating == 'asc':
                stmt = stmt.order_by(Recipe.average_rating)
        res = await self.db.execute(stmt)
        recipes = res.scalars().all()
        return recipes

    async def create(self, recipe_data: RecipeCreate) -> Recipe:
        recipe = Recipe(
            title=recipe_data.title,
            description=recipe_data.description,
            total_time=sum([step.step_time for step in recipe_data.steps], datetime.timedelta(0))
        )
        self.db.add(recipe)
        return recipe

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
