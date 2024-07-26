from fastapi import Depends

from app.repositories.image import ImageRepository
from app.repositories.recipe import RecipeRepository
from app.repositories.step import StepRepository
from app.services.step import StepService


class ImageService:
    def __init__(self,
                 image_repository: ImageRepository = Depends(),
                 recipe_repository: RecipeRepository = Depends(),
                 step_repository: StepRepository = Depends(),
                 step_service: StepService = Depends()
                 ):
        self.image_repository = image_repository
        self.recipe_repository = recipe_repository
        self.step_repository = step_repository
        self.step_service = step_service

    async def add_recipe_image(self, image_id: str, image_url: str, recipe_title: str):
        recipe = await self.recipe_repository.get(title=recipe_title, by_title=True)
        image_exists = recipe.image
        if not image_exists:
            await self.image_repository.create(image_id, image_url)
        else:
            current_image_image_id = image_exists.id
            await self.image_repository.update(image_id, image_url, current_image_image_id=current_image_image_id)

    async def add_step_image(self, image_id: str, image_url: str, recipe_title: str, step_number: int):
        recipe_id = await self.recipe_repository.get_recipe_id(recipe_title)
        step = await self.step_repository.get_step_id_and_image(recipe_id, step_number)
        image_exists = step[1]
        if not image_exists:
            await self.image_repository.create(image_id, image_url, step[0])
            await self.step_service.add_image(image_id, recipe_id, step_number)
        else:
            await self.image_repository.update(image_id, image_url, step_id=step[0])
            await self.step_service.add_image(image_id, recipe_id, step_number)

    async def get_recipe_image_url(self, recipe_title: str) -> str:
        return await self.image_repository.get_recipe_image_url(recipe_title)

    async def get_recipe_image_id(self, recipe_title: str) -> str:
        return await self.image_repository.get_recipe_image_id(recipe_title)

    async def get_step_image_id(self, recipe_id: int, step_number: int) -> str:
        return await self.image_repository.get_step_image_id(recipe_id, step_number)
