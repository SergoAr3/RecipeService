import datetime

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Step
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

    async def update(self, step: StepCreate, step_description: str) -> None:
        await self.db.execute(
            update(Step).where(Step.description == step_description).values(
                number=step.number,
                description=step.description,
                step_time=step.step_time))
        print(f'Добавлено для: number: {step.number}, description: {step.description}, step_time: {step.step_time}')
