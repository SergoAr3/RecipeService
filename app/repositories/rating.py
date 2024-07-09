from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Rating, Recipe


class RatingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, recipe_id: int = None, recipe_title: str = None, by_recipe_id: bool = False) -> List[Rating]:
        if by_recipe_id:
            stmt = (select(Rating).where(Rating.id == recipe_id))
        else:
            stmt = (select(Rating).select_from(Rating)
                    .join(Recipe, Recipe.id == Rating.recipe_id)
                    .where(Recipe.title == recipe_title))
        res = await self.db.execute(stmt)
        ratings = res.scalars().all()
        return ratings

    async def create(self, rating: int, user_id: int, recipe_title: str) -> Rating:
        recipe = await self.db.execute(select(Recipe).where(Recipe.title == recipe_title))
        recipe = recipe.scalars().first()
        db_rating = Rating(
            rating=rating,
            user_id=user_id,
            recipe_id=recipe.id
        )
        rating_exists = await self.db.execute(select(Rating).where(Rating.user_id == db_rating.user_id,
                                                                   Rating.recipe_id == db_rating.recipe_id))
        rating_exists = rating_exists.scalars().first()
        if not rating_exists:
            self.db.add(db_rating)
        else:
            await self.db.execute(update(Rating).where(Rating.user_id == db_rating.user_id,
                                                       Rating.recipe_id == db_rating.recipe_id).values(
                rating=rating))
        return db_rating

    # async def delete(self, rating: RatingCreate) -> None:
    #     await self.db.delete(rating)
    #
    # async def update(self, step: StepCreate, recipe_id: int) -> None:
    #     await self.db.execute(update(Step).where(Step.recipe_id == recipe_id).values(number=step.number,
    #                                                                                  description=step.description,
    #                                                                                  step_time=step.step_time))
