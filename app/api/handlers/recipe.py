import datetime
import shutil
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Query
from fastapi.responses import RedirectResponse

from app.api.handlers.auth import fastapi_users
from app.db import User
from app.schemas.rating import RatingCreate
from app.schemas.recipe import RecipeCreate
from app.repositories.google_drive.google_drive import GoogleDriveRepository
from app.services.recipe import RecipeService
from app.services.rating import RatingService

recipe_router = APIRouter()
current_user = fastapi_users.current_user()


@recipe_router.post("/image/{recipe_title}")
async def upload_image(
        recipe_title: str,
        file: UploadFile,
        google_drive_repository: Annotated[GoogleDriveService, Depends()],
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(current_user)
):
    temp_file_path = f'/tmp/{file.filename}'
    with open(temp_file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_id = google_drive_repository.upload_image(file.filename, temp_file_path)
    await recipe_service.add_image(recipe_title, f'https://drive.google.com/uc?id={file_id}')
    return file


@recipe_router.get('/image/{recipe_tite}')
async def get_recipe_image(
        recipe_tite: str,
        recipe_service: Annotated[RecipeService, Depends()]
):
    recipe = await recipe_service.get_recipe_by_title(recipe_tite)
    return RedirectResponse(url=recipe.image_url)


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
    if ingredient_name:
        return await recipe_service.get_by_ingredient(ingredient_name)

    elif min_time and max_time:
        return await recipe_service.get_by_total_time(min_time=min_time, max_time=max_time)
    elif min_time:
        return await recipe_service.get_by_total_time(min_time=min_time)
    elif max_time:
        return await recipe_service.get_by_total_time(max_time=max_time)
    elif min_rating:
        return await recipe_service.get_by_average_rating(min_rating=min_rating)
    elif max_rating:
        return await recipe_service.get_by_average_rating(max_rating=max_rating)
    elif sort_time == 'desc':
        return await recipe_service.get_by_total_time(sort_by_time=True, descending=True)
    elif sort_time == 'asc':
        return await recipe_service.get_by_total_time(sort_by_time=True)
    elif sort_rating == 'desc':
        return await recipe_service.get_by_average_rating(sort_by_rating=True, descending=True)
    elif sort_rating == 'asc':
        return await recipe_service.get_by_average_rating(sort_by_rating=True)


@recipe_router.delete('/')
async def delete_recipe(
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(current_user)
):
    return await recipe_service.delete_recipe(recipe_id)


@recipe_router.post('/')
async def create_recipe(
        recipe: RecipeCreate,
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(current_user),
):
    await recipe_service.create_recipe(recipe)


@recipe_router.put('/')
async def update_recipe(
        recipe: RecipeCreate,
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
        user: User = Depends(current_user)
):
    return await recipe_service.update_recipe(recipe, recipe_id)


@recipe_router.put('/rate/{recipe_title}')
async def rate_recipe(
        recipe_title: str,
        rating: RatingCreate,
        rating_service: Annotated[RatingService, Depends()],
        user: User = Depends(current_user)
):
    return await rating_service.create_rating(rating, user.id, recipe_title)
