import datetime
import shutil
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, UploadFile
from starlette.responses import StreamingResponse
from transliterate import translit

import app.api.errors.level_200 as msg
import app.api.errors.level_400 as err
from app.auth.utils import get_current_active_auth_user
from app.db import User
from app.repositories.google_drive.google_drive import GoogleDriveRepository
from app.schemas.rating import RatingCreate
from app.schemas.recipe import RecipeCreate
from app.services.image import ImageService
from app.services.rating import RatingService
from app.services.recipe import RecipeService


recipe_router = APIRouter()


@recipe_router.get('/image/{recipe_title}')
async def get_recipe_image(
        recipe_title: str,
        image_service: Annotated[ImageService, Depends()],
        recipe_service: Annotated[RecipeService, Depends()],
        google_drive_repository: Annotated[GoogleDriveRepository, Depends()],

):
    try:
        recipe = await recipe_service.get_recipe_by_title(recipe_title)
    except AttributeError:
        raise err.HTTP_404_NOT_FOUND_recipe
    image_id = await image_service.get_image_id(recipe.id)
    if not image_id:
        raise err.HTTP_404_NOT_FOUND_image

    image_stream = await google_drive_repository.download_image(image_id)

    image_stream.seek(0)
    return StreamingResponse(image_stream, media_type="image/jpeg")


@recipe_router.get('/image/{recipe_title}/download/')
async def download_recipe_image(
        recipe_title: str,
        image_service: Annotated[ImageService, Depends()],
        recipe_service: Annotated[RecipeService, Depends()],
        google_drive_repository: Annotated[GoogleDriveRepository, Depends()],

):
    try:
        recipe = await recipe_service.get_recipe_by_title(recipe_title)
    except AttributeError:
        raise err.HTTP_404_NOT_FOUND_recipe
    image_id = await image_service.get_image_id(recipe.id)
    if not image_id:
        raise err.HTTP_404_NOT_FOUND_image

    image_stream = await google_drive_repository.download_image(image_id)
    image_stream.seek(0)
    image_name = translit(recipe_title, language_code='ru', reversed=True)
    return StreamingResponse(image_stream, media_type="image/jpeg",
                             headers={"Content-Disposition": f"attachment; filename={image_name}.jpg"})


@recipe_router.get('/all_recipes')
async def get_all_recipes(
        recipe_service: Annotated[RecipeService, Depends()]
):
    all_recipes = await recipe_service.get_all_recipes()
    if not all_recipes:
        raise msg.HTTP_204_NO_CONTENT
    return all_recipes


@recipe_router.get('/{recipe_id}')
async def get_recipe(
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
):
    try:
        recipe = await recipe_service.get_recipe(recipe_id)
    except AttributeError:
        raise err.HTTP_404_NOT_FOUND_recipe
    return recipe


@recipe_router.get('/')
async def get_recipes_filter(
        recipe_service: Annotated[RecipeService, Depends()],
        ingredient_name: Annotated[str | None, Query()] = None,
        min_time: Annotated[
            datetime.timedelta | None, Query(description='HH:MM:SS', example='00:00:00')] = None,
        max_time: Annotated[
            datetime.timedelta | None, Query(description='HH:MM:SS', example='00:00:00')] = None,
        max_rating: Annotated[float | None, Query(ge=1, le=5)] = None,
        min_rating: Annotated[float | None, Query(ge=1, le=5)] = None,
        sort_time: Annotated[Literal['desc', 'asc'] | None, Query(description='desc or asc')] = None,
        sort_rating: Annotated[Literal['desc', 'asc'] | None, Query(description='desc or asc')] = None
):
    return await recipe_service.get_filtered_recipes(
        ingredient_name=ingredient_name,
        min_time=min_time,
        max_time=max_time,
        max_rating=max_rating,
        min_rating=min_rating,
        sort_time=sort_time,
        sort_rating=sort_rating
    )


@recipe_router.delete('/')
async def delete_recipe(
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    await recipe_service.delete_recipe(recipe_id)

    return msg.HTTP_200_OK_deleted


@recipe_router.post('/')
async def create_recipe(
        recipe: RecipeCreate,
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    await recipe_service.create_recipe(recipe)
    return msg.HTTP_200_OK_created


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
    try:
        await image_service.add_image(file_id, f'https://drive.google.com/uc?id={file_id}', recipe_title)
    except AttributeError:
        raise err.HTTP_404_NOT_FOUND_recipe
    return file


@recipe_router.put('/')
async def update_recipe(
        recipe: RecipeCreate,
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    update_recipe = await recipe_service.update_recipe(recipe, recipe_id)
    if not update_recipe:
        raise err.HTTP_404_NOT_FOUND_recipe
    return msg.HTTP_200_OK_updated


@recipe_router.put('/rate/{recipe_title}')
async def rate_recipe(
        recipe_title: str,
        rating: RatingCreate,
        rating_service: Annotated[RatingService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    create_rating = await rating_service.create_rating(rating, user.id, recipe_title)
    if not create_rating:
        raise err.HTTP_404_NOT_FOUND_recipe
    return msg.HTTP_200_OK_rating
