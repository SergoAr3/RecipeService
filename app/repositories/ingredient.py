from typing import List

from fastapi import Depends
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Ingredient
from app.db.db import get_db
from app.schemas.ingredient import IngredientCreate


class IngredientRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all(self) -> list[Ingredient]:
        stmt = select(Ingredient)
        res = await self.db.execute(stmt)
        recipes = res.scalars().all()
        return recipes

    async def get(self, condition: int | str,
                  by_recipe_id: bool = False, by_name: bool = False) -> Ingredient | List[Ingredient]:
        if by_recipe_id:
            stmt = select(Ingredient).where(Ingredient.recipe_id == condition)
        elif by_name:
            stmt = select(Ingredient).where(Ingredient.name == condition)
        else:
            stmt = select(Ingredient).where(Ingredient.id == condition)
            res = await self.db.execute(stmt)
            ingredient = res.scalar()
            return ingredient
        res = await self.db.execute(stmt)
        ingredients = res.scalars().all()
        return ingredients

    async def create(self, ingredient: IngredientCreate, recipe_id: int) -> Ingredient:
        db_ingredient = Ingredient(
            name=ingredient.name,
            quantity=ingredient.quantity,
            recipe_id=recipe_id
        )
        self.db.add(db_ingredient)
        return db_ingredient

    async def delete(self, ingredient_name: str, recipe_id: int) -> None:
        ingredient = await self.db.execute(
            select(Ingredient)
            .where(and_(Ingredient.recipe_id == recipe_id, Ingredient.name == ingredient_name)))
        ingredient = ingredient.scalar()

        await self.db.delete(ingredient)

    async def update(self, ingredient_update_data: dict, recipe_id: int, ingredient_name: str) -> None:
        await self.db.execute(update(Ingredient)
                              .where(and_(Ingredient.recipe_id == recipe_id, Ingredient.name == ingredient_name))
                              .values(ingredient_update_data))
