from fastapi import Depends

from app.db import Image
from app.repositories.image import ImageRepository
from app.repositories.recipe import RecipeRepository


class ImageService:
    def __init__(self,
                 image_repository: ImageRepository = Depends(),
                 recipe_repository: RecipeRepository = Depends()
                 ):
        self.image_repository = image_repository
        self.recipe_repository = recipe_repository

    async def add_image(self, image_id: str, image_url: str, recipe_title: str) -> Image:
        recipe = await self.recipe_repository.get(title=recipe_title, by_title=True)
        image = Image(
            id=image_id,
            url=image_url,
            recipe_id=recipe.id
        )
        image_exists = recipe.image
        if not image_exists:
            await self.image_repository.create(image_id, image_url, recipe.id)
        else:
            current_image_recipe_id = image_exists[0].recipe_id
            await self.image_repository.update(current_image_recipe_id, image_id, image_url)
        return image

    async def get_image_url(self, recipe_id: int) -> str:
        return await self.image_repository.get_image_url(recipe_id)

    async def get_image_id(self, recipe_id: int) -> str:
        return await self.image_repository.get_image_id(recipe_id)
