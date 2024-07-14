import datetime
import shutil
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Query
from fastapi.responses import RedirectResponse

from app.auth.utils import get_current_active_auth_user
from app.db import User
from app.schemas.rating import RatingCreate
from app.schemas.recipe import RecipeCreate
from app.repositories.google_drive.google_drive import GoogleDriveRepository
from app.services.image import ImageService
from app.services.recipe import RecipeService
from app.services.rating import RatingService

recipe_router = APIRouter()


@recipe_router.post("/image/{recipe_title}")
async def upload_image(
        recipe_title: str,
        file: UploadFile,
        google_drive_repository: Annotated[GoogleDriveRepository, Depends()],
        image_service: Annotated[ImageService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    temp_file_path = f'/tmp/{file.filename}'
    with open(temp_file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_id = google_drive_repository.upload_image(file.filename, temp_file_path)
    await image_service.add_image(file_id, f'https://drive.google.com/uc?id={file_id}', recipe_title )
    return file


@recipe_router.get('/image/{recipe_tite}')
async def get_recipe_image(
        recipe_tite: str,
        image_service: Annotated[ImageService, Depends()],
        recipe_service: Annotated[RecipeService, Depends()]
):
    recipe = await recipe_service.get_recipe_by_title(recipe_tite)
    image_url = await image_service.get_image_url(recipe.id)
    return RedirectResponse(url=image_url)


@recipe_router.get('/all_recipes')
async def get_all_recipes(
        recipe_service: Annotated[RecipeService, Depends()]
):
    return await recipe_service.get_all_recipes()


@recipe_router.get('/{recipe_id}')
async def get_recipe(
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
):
    recipe = await recipe_service.get_recipe(recipe_id)
    return recipe


@recipe_router.get('/')
async def get_recipes_filter(
        recipe_service: Annotated[RecipeService, Depends()],
        ingredient_name: str | None = None,
        min_time: Annotated[
            datetime.timedelta | None, Query(description='HH:MM:SS')] = None,
        max_time: Annotated[
            datetime.timedelta | None, Query(description='HH:MM:SS')] = None,
        max_rating: float | None = None,
        min_rating: float | None = None,
        sort_time: Annotated[str | None, Query(description='desc or asc')] = None,
        sort_rating: Annotated[str | None, Query(description='desc or asc')] = None
):
    return await recipe_service.get_filtered_recipes(
        ingredient_name,
        min_time,
        max_time,
        max_rating,
        min_rating,
        sort_time,
        sort_rating
    )


@recipe_router.delete('/')
async def delete_recipe(
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    return await recipe_service.delete_recipe(recipe_id)


@recipe_router.post('/')
async def create_recipe(
        recipe: RecipeCreate,
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    await recipe_service.create_recipe(recipe)


@recipe_router.put('/')
async def update_recipe(
        recipe: RecipeCreate,
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    return await recipe_service.update_recipe(recipe, recipe_id)


@recipe_router.put('/rate/{recipe_title}')
async def rate_recipe(
        recipe_title: str,
        rating: RatingCreate,
        rating_service: Annotated[RatingService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    return await rating_service.create_rating(rating, user.id, recipe_title)
