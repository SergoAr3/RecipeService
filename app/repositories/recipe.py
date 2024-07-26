import datetime
from typing import List

from fastapi import Depends
from sqlalchemy import desc, or_, select, update
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

    async def get_recipe_id(self, title: str):
        stmt = select(Recipe.id).where(Recipe.title == title)
        res = await self.db.execute(stmt)
        recipe = res.scalar()
        print(recipe)
        return recipe

    async def get_filtered_recipes(
            self,
            recipes_id: list[Recipe],
            min_time: datetime.timedelta | None,
            max_time: datetime.timedelta | None,
            max_rating: float | None,
            min_rating: float | None,
            sort_time: str | None,
            sort_rating: str | None,
    ) -> list[Recipe] | None:
        min_time = min_time if min_time is not None else datetime.timedelta(seconds=0)
        max_time = max_time if max_time is not None else datetime.timedelta(weeks=4)
        max_rating = max_rating if max_rating is not None else 5
        min_rating = min_rating if min_rating is not None else 0
        sort_time = sort_time if sort_time is not None else 'desc'
        sort_rating = sort_rating if sort_rating is not None else 'desc'

        stmt = (
            select(Recipe)
            .where(Recipe.total_time >= min_time, Recipe.total_time <= max_time,
                   Recipe.average_rating >= min_rating, Recipe.average_rating <= max_rating)
        )

        if recipes_id:
            conditions = [Recipe.id == recipe_id for recipe_id in recipes_id]
            stmt = stmt.where(or_(*conditions))

        if sort_time == 'desc':
            stmt = stmt.order_by(desc(Recipe.total_time))
        elif sort_time == 'asc':
            stmt = stmt.order_by(Recipe.total_time)

        if sort_rating == 'desc':
            stmt = stmt.order_by(desc(Recipe.average_rating))
        elif sort_rating == 'asc':
            stmt = stmt.order_by(Recipe.average_rating)

        res = await self.db.execute(stmt)
        recipes = res.scalars().all()
        return recipes

    async def create(self, recipe_data: RecipeCreate) -> Recipe | None:
        check_recipe = await self.get(title=recipe_data.title, by_title=True)
        if check_recipe:
            return None
        recipe = Recipe(
            title=recipe_data.title,
            description=recipe_data.description,
            total_time=sum([step.step_time for step in recipe_data.steps], datetime.timedelta(0))
        )
        self.db.add(recipe)
        return recipe

    async def delete(self, recipe: Recipe) -> None:
        await self.db.delete(recipe)

    async def update(self, recipe_update_data: dict, recipe_id: int = None, recipe_title: str = None) -> None:
        if recipe_id:
            await self.db.execute(update(Recipe).where(Recipe.id == recipe_id).values(recipe_update_data))
        else:
            await self.db.execute(update(Recipe).where(Recipe.title == recipe_title).values(recipe_update_data))

    async def update_rating(self, recipe_title: str, rating: float):
        await self.db.execute(update(Recipe).where(Recipe.title == recipe_title).values(average_rating=rating))
