from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Step
from app.schemas.step import StepCreate


class StepRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, recipe_id: int) -> list[Step]:
        stmt = select(Step).where(Step.recipe_id == recipe_id)
        res = await self.db.execute(stmt)
        recipes = res.scalars().all()
        return recipes

    async def get(self, recipe_id: int, number: int) -> Step:
        stmt = select(Step).where(Step.recipe_id == recipe_id, Step.number == number)
        res = await self.db.execute(stmt)
        step = res.scalars().first()
        return step

    async def create(self, step: StepCreate, recipe_id: int) -> Step:
        db_step = Step(
            number=step.number,
            description=step.description,
            step_time=step.step_time,
            recipe_id=recipe_id
        )
        self.db.add(db_step)
        return db_step

    async def delete(self, step: StepCreate) -> None:
        await self.db.delete(step)

    async def update(self, step: StepCreate, recipe_id: int, step_description: str) -> None:
        await self.db.execute(
            update(Step).where(Step.description == step_description).values(
                number=step.number,
                description=step.description,
                step_time=step.step_time))
        print(f'Добавлено для: number: {step.number}, description: {step.description}, step_time: {step.step_time}')
