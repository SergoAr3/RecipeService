from app.repositories.step import StepRepository
from app.schemas.step import StepCreate, StepRead


class StepService:
    def __init__(self, step_repository: StepRepository):
        self.step_repository = step_repository

    async def get_all_steps(self, recipe_id: int) -> StepRead:
        step = await self.step_repository.get_all(recipe_id)
        step = StepRead.from_orm(step)
        return step

    async def get_step(self, recipe_id: int, number: int) -> StepRead:
        step = await self.step_repository.get(recipe_id, number)
        step = StepRead.from_orm(step)
        return step

    async def create_step(self, step: StepCreate, recipe_id: int) -> None:
        db_step = await self.step_repository.create(step, recipe_id)
