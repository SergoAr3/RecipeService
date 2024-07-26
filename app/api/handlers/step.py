from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from starlette import status

import app.api.errors as err
from app.auth.utils import get_current_active_auth_user
from app.repositories.google_drive.google_drive import GoogleDriveRepository
from app.schemas.step import StepCreate, StepUpdate
from app.services.image import ImageService
from app.services.recipe import RecipeService
from app.services.step import StepService


step_router = APIRouter(dependencies=[Depends(get_current_active_auth_user)])


@step_router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_step(
        step: StepCreate,
        recipe_id: int,
        step_service: Annotated[StepService, Depends()],
):
    try:
        await step_service.create_step(step, recipe_id)
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@step_router.delete('/{recipe_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_step(
        recipe_id: int,
        step_number: int,
        step_service: Annotated[StepService, Depends()],
):
    try:
        await step_service.delete_step(step_number, recipe_id)
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@step_router.patch('/{recipe_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_step(
        step: StepUpdate,
        recipe_id: int,
        step_number: int,
        step_service: Annotated[StepService, Depends()],
):
    try:
        await step_service.update_step(step, recipe_id, step_number)
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR


@step_router.post("/image", status_code=status.HTTP_204_NO_CONTENT)
async def upload_image(
        recipe_title: str,
        step_number: int,
        file: UploadFile,
        google_drive_repository: Annotated[GoogleDriveRepository, Depends()],
        image_service: Annotated[ImageService, Depends()],
):
    try:
        file_id = google_drive_repository.upload_image(file)
        await image_service.add_step_image(file_id, f'https://drive.google.com/uc?id={file_id}', recipe_title,
                                           step_number)
    except IndexError:
        raise err.HTTP_404_NOT_FOUND_RECIPE
    return file


@step_router.get('/image/{recipe_title}/{step_number}')
async def get_step_image(
        recipe_title: str,
        step_number: int,
        image_service: Annotated[ImageService, Depends()],
        recipe_service: Annotated[RecipeService, Depends()],
        google_drive_repository: Annotated[GoogleDriveRepository, Depends()],
):
    try:
        recipe_id = await recipe_service.get_recipe_id_by_name(recipe_title)
        if not recipe_id:
            raise err.HTTP_404_NOT_FOUND_RECIPE
        image_id = await image_service.get_step_image_id(recipe_id, step_number)
        if not image_id:
            raise err.HTTP_404_NOT_FOUND_IMAGE
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise err.HTTP_500_INTERNAL_ERROR

    image_stream = await google_drive_repository.download_image(image_id)

    image_stream.seek(0)
    return StreamingResponse(image_stream, media_type="image/jpeg")
