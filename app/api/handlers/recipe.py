import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
from loguru import logger
from starlette import status
from transliterate import translit

import app.api.errors as err
from app.auth.utils import get_current_active_auth_user
from app.db import User
from app.repositories.google_drive.google_drive import GoogleDriveRepository
from app.schemas.recipe import RecipeCreate, RecipeUpdate
from app.services.image import ImageService
from app.services.rating import RatingService
from app.services.recipe import RecipeService


recipe_router = APIRouter()
protected_router = APIRouter(dependencies=[Depends(get_current_active_auth_user)])


@recipe_router.get('/all', status_code=status.HTTP_200_OK)
async def get_all_recipes(
        recipe_service: Annotated[RecipeService, Depends()]
):
    try:
        all_recipes = await recipe_service.get_recipes()
        return {'recipes': all_recipes}
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@recipe_router.get('/{recipe_id}', status_code=status.HTTP_200_OK)
async def get_recipe(
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
):
    try:
        recipe = await recipe_service.get_recipe(recipe_id)
    except AttributeError:
        raise err.HTTP_404_NOT_FOUND_RECIPE
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR

    return {'recipe': recipe}


@recipe_router.get('')
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
    try:
        recipes = await recipe_service.get_filtered_recipes(
            ingredient_name=ingredient_name,
            min_time=min_time,
            max_time=max_time,
            max_rating=max_rating,
            min_rating=min_rating,
            sort_time=sort_time,
            sort_rating=sort_rating
        )
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR

    return {'recipes': recipes}


@protected_router.delete('/{recipe_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
):
    try:
        await recipe_service.delete_recipe(recipe_id)
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@protected_router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_recipe(
        recipe: RecipeCreate,
        recipe_service: Annotated[RecipeService, Depends()],
):
    try:
        await recipe_service.create_recipe(recipe)
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@protected_router.patch('/{recipe_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_recipe(
        recipe: RecipeUpdate,
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends()],
):
    try:
        await recipe_service.update_recipe(recipe, recipe_id)
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@protected_router.put('/rate/{recipe_title}', status_code=status.HTTP_204_NO_CONTENT)
async def rate_recipe(
        recipe_title: str,
        rating: float,
        rating_service: Annotated[RatingService, Depends()],
        user: User = Depends(get_current_active_auth_user),
):
    try:
        await rating_service.create_rating(rating, user.id, recipe_title)
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@protected_router.post("/image", status_code=status.HTTP_204_NO_CONTENT)
async def upload_image(
        recipe_title: str,
        file: UploadFile,
        google_drive_repository: Annotated[GoogleDriveRepository, Depends()],
        image_service: Annotated[ImageService, Depends()],
        recipe_service: Annotated[RecipeService, Depends()]
):
    try:
        file_id = google_drive_repository.upload_image(file)
        await image_service.add_recipe_image(file_id, f'https://drive.google.com/uc?id={file_id}', recipe_title)
        await recipe_service.add_image(file_id, recipe_title)
    except AttributeError:
        raise err.HTTP_404_NOT_FOUND_RECIPE
    except TimeoutError:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise err.HTTP_500_INTERNAL_ERROR


@recipe_router.get('/image/{recipe_title}')
async def get_recipe_image(
        recipe_title: str,
        image_service: Annotated[ImageService, Depends()],
        recipe_service: Annotated[RecipeService, Depends()],
        google_drive_repository: Annotated[GoogleDriveRepository, Depends()],

):
    try:
        recipe_id = await recipe_service.get_recipe_id_by_name(recipe_title)
        if not recipe_id:
            raise err.HTTP_404_NOT_FOUND_RECIPE
        image_id = await image_service.get_recipe_image_id(recipe_title)
        if not image_id:
            raise err.HTTP_404_NOT_FOUND_IMAGE
        image_stream = await google_drive_repository.download_image(image_id)
        image_stream.seek(0)
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR
    return StreamingResponse(image_stream, media_type="image/jpeg")


@recipe_router.get('/image/{recipe_title}/download/')
async def download_recipe_image(
        recipe_title: str,
        image_service: Annotated[ImageService, Depends()],
        recipe_service: Annotated[RecipeService, Depends()],
        google_drive_repository: Annotated[GoogleDriveRepository, Depends()],

):
    try:
        recipe_id = await recipe_service.get_recipe_id_by_name(recipe_title)
        if not recipe_id:
            raise err.HTTP_404_NOT_FOUND_RECIPE

        image_id = await image_service.get_recipe_image_id(recipe_title)
        if not image_id:
            raise err.HTTP_404_NOT_FOUND_IMAGE
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR

    image_stream = await google_drive_repository.download_image(image_id)
    image_stream.seek(0)
    image_name = translit(recipe_title, language_code='ru', reversed=True)
    return StreamingResponse(image_stream, media_type="image/jpeg",
                             headers={"Content-Disposition": f"attachment; filename={image_name}.jpg"})
