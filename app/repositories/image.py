from typing import List

from fastapi import Depends
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import ImageRecipe, ImageStep, Rating, Recipe, Step
from app.db.db import get_db


class ImageRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
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

    async def create(self, image_id: str, image_url: str, step_id: int = None):
        if step_id:
            image = ImageStep(
                id=image_id,
                url=image_url,
                step_id=step_id)
        else:
            image = ImageRecipe(
                id=image_id,
                url=image_url)
        self.db.add(image)
        return image

    async def update(self, image_id: str, image_url: str, current_image_image_id: str = None, step_id: int = None):
        if current_image_image_id:
            await self.db.execute(
                update(ImageRecipe).where(ImageRecipe.id == current_image_image_id).values(id=image_id,
                                                                                           url=image_url))
        else:
            await self.db.execute(
                update(ImageStep).where(ImageStep.step_id == step_id).values(id=image_id,
                                                                             url=image_url))

    async def get_recipe_image_url(self, recipe_title: str) -> str:
        stmt = (select(Recipe.image_id).where(Recipe.title == recipe_title))
        res = await self.db.execute(stmt)
        image_id = res.scalar()
        stmt = (select(ImageRecipe.url).where(ImageRecipe.id == image_id))
        res = await self.db.execute(stmt)
        image_url = res.scalar()

        return image_url

    async def get_recipe_image_id(self, recipe_title: str):
        stmt = (select(Recipe.image_id).where(Recipe.title == recipe_title))
        res = await self.db.execute(stmt)
        image_id = res.scalar()

        return image_id

    async def get_step_image_id(self, recipe_id: int, step_number: int):
        res = await self.db.execute(
            select(Step.image_id).where(and_(Step.recipe_id == recipe_id, Step.number == step_number)))
        image_id = res.scalar()

        return image_id
