import datetime

from fastapi import Depends
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Recipe, Step
from app.db.db import get_db
from app.schemas.step import StepCreate


class StepRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all(self, recipe_id: int) -> list[Step]:
        stmt = select(Step).where(Step.recipe_id == recipe_id)
        res = await self.db.execute(stmt)
        steps = res.scalars().all()
        return steps

    async def get(self, recipe_id: int, number: int) -> Step:
        stmt = select(Step).where(Step.recipe_id == recipe_id, Step.number == number)
        res = await self.db.execute(stmt)
        step = res.scalar()
        return step

    async def get_step_id_and_image(self, recipe_id: int, number: int):
        stmt = select(Step.id, Step.image_id).where(Step.recipe_id == recipe_id, Step.number == number)
        res = await self.db.execute(stmt)
        step = res.fetchall()[0]
        return step

    async def create(self, step: StepCreate, recipe_id: int) -> Step:
        db_step = Step(
            number=step.number,
            description=step.description,
            step_time=step.step_time,
            recipe_id=recipe_id
        )
        self.db.add(db_step)

        recipe = await self.db.execute(select(Recipe).where(Recipe.id == recipe_id))
        recipe = recipe.scalar()

        await self.db.execute(
            update(Recipe).where(Recipe.id == recipe_id).values(total_time=recipe.total_time + step.step_time)
        )
        return db_step

    async def delete(self, step_number: int, recipe_id: int) -> None:
        step = await self.db.execute(select(Step).where(and_(Step.number == step_number, Step.recipe_id == recipe_id)))
        step = step.scalar()
        await self.db.delete(step)

    async def update(self, step_update_data: dict, recipe_id: int, step_number: int) -> None:
        await self.db.execute(
            update(Step).where(and_(Step.recipe_id == recipe_id, Step.number == step_number)).values(
                step_update_data))

        updated_recipe = await self.db.execute(select(Recipe).where(Recipe.id == recipe_id))
        updated_recipe = updated_recipe.scalar()
        updated_recipe_steps = updated_recipe.steps
        updated_total_time = sum([step.step_time for step in updated_recipe_steps], datetime.timedelta(seconds=0))

        await self.db.execute(
            update(Recipe).where(Recipe.id == recipe_id).values(total_time=updated_total_time)
        )
