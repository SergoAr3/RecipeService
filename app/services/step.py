from fastapi import Depends

import app.api.errors as err
from app.repositories.recipe import RecipeRepository
from app.repositories.step import StepRepository
from app.schemas.step import StepCreate, StepRead, StepUpdate


class StepService:
    def __init__(self,
                 step_repository: StepRepository = Depends(),
                 recipe_repository: RecipeRepository = Depends()
                 ):
        self.step_repository = step_repository
        self.recipe_repository = recipe_repository

    async def get_all_steps(self, recipe_id: int) -> StepRead:
        step = await self.step_repository.get_all(recipe_id)
        step = StepRead.from_orm(step)
        return step

    async def get_step(self, recipe_id: int, number: int) -> StepRead:
        step = await self.step_repository.get(recipe_id, number)
        step = StepRead.from_orm(step)
        return step

    async def create_step(self, step: StepCreate, recipe_id: int) -> None:
        await self.step_repository.create(step, recipe_id)

    async def update_step(self, step: StepUpdate, recipe_id: int, step_number: int):
        db_recipe = await self.recipe_repository.get(recipe_id)
        db_step = await self.step_repository.get(recipe_id, step_number)
        if db_recipe and db_step:
            step_update_data = step.model_dump(exclude_unset=True)
            await self.step_repository.update(step_update_data, recipe_id, step_number)
        else:
            raise err.HTTP_404_NOT_FOUND_RECIPE_OR_STEP

    async def delete_step(self, step_number: int, recipe_id: int):
        await self.step_repository.delete(step_number, recipe_id)

    async def add_image(self, image_id: str, recipe_id: int, step_number: int):
        step_update_data = {'image_id': image_id}
        await self.step_repository.update(step_update_data, recipe_id, step_number)
