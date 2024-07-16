from typing import List

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Image, Rating, Recipe
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

    async def create(self, image_id: str, image_url: str, recipe_id: int) -> Image:
        image = Image(
            id=image_id,
            url=image_url,
            recipe_id=recipe_id
        )
        self.db.add(image)
        return image

    async def update(self, current_image_recipe_id: int, image_id: str, image_url: str):
        await self.db.execute(
            update(Image).where(Image.recipe_id == current_image_recipe_id).values(id=image_id, url=image_url))

    async def get_image_url(self, recipe_id: int) -> str:
        stmt = (select(Image.url).where(Image.recipe_id == recipe_id))
        res = await self.db.execute(stmt)
        image_url = res.scalar()

        return image_url

    async def get_image_id(self, recipe_id: int) -> str:
        stmt = (select(Image.id).where(Image.recipe_id == recipe_id))
        res = await self.db.execute(stmt)
        image_url = res.scalar()

        return image_url
