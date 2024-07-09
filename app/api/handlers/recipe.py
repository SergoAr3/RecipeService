import shutil
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import RedirectResponse

from app.api.handlers.auth import fastapi_users
from app.db import User
from app.schemas.recipe import RecipeCreate
from app.services.google_drive.google_drive import GoogleDriveService
from app.services.recipe import RecipeService
from app.services.rating import RatingService
from app.api.dependencies import recipe_service_dp, rating_service_dp, google_drive_service_dp

recipe_router = APIRouter()
current_user = fastapi_users.current_user()


@recipe_router.post("/file/upload-file/{recipe_title}")
async def upload_file(
        recipe_title: str,
        file: UploadFile,
        google_drive_service: Annotated[GoogleDriveService, Depends(google_drive_service_dp)],
        recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)],
        user: User = Depends(current_user)
):
    temp_file_path = f'/tmp/{file.filename}'
    with open(temp_file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_id = google_drive_service.upload_image(file.filename, temp_file_path)
    await recipe_service.add_image(recipe_title, f'https://drive.google.com/uc?id={file_id}')
    return file


@recipe_router.get('/get_recipe_image/{recipe_tite}')
async def get_recipe_image(
        recipe_tite: str,
        recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    recipe = await recipe_service.get_recipe_by_title(recipe_tite)
    return RedirectResponse(url=recipe.image_url)


@recipe_router.get('/all_recipes')
async def get_all_recipes(recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    return await recipe_service.get_all_recipes()


@recipe_router.get('/get_recipe/{recipe_id}')
async def get_recipe(
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)],
):
    recipe = await recipe_service.get_recipe(recipe_id)
    return recipe


@recipe_router.get('/get_recipe/filter/ingredient/{ingredient_name}')
async def get_recipe_by_ingredient(ingredient_name: str,
                                   recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    recipes = await recipe_service.get_by_ingredient(ingredient_name)
    return recipes


@recipe_router.get('/get_recipe/filter/total_time/min/{min_time}')
async def get_recipe_by_min_time(min_time: int,
                                 recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    return await recipe_service.get_by_total_time(min_time=min_time)


@recipe_router.get('/get_recipe/filter/total_time/max/{max_time}')
async def get_recipe_by_max_time(max_time: int,
                                 recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    return await recipe_service.get_by_total_time(max_time=max_time)


@recipe_router.get('/get_recipe/sort/by_time/desc')
async def get_recipe_by_time_desc(recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    return await recipe_service.get_by_total_time(sort_by_time=True, descending=True)


@recipe_router.get('/get_recipe/sort/by_time/asc')
async def get_recipe_by_time_asc(recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    return await recipe_service.get_by_total_time(sort_by_time=True)


@recipe_router.get('/get_recipe/filter/average_rating/min/{min_rate}')
async def get_recipe_by_min_rate(min_rate: int,
                                 recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    return await recipe_service.get_by_average_rating(min_rate=min_rate)


@recipe_router.get('/get_recipe/filter/average_rating/max/{max_rate}')
async def get_recipe_by_max_rate(max_rate: int,
                                 recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    return await recipe_service.get_by_average_rating(max_rate=max_rate)


@recipe_router.get('/get_recipe/sort/average_rating/desc')
async def get_recipe_by_rate_desc(recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    return await recipe_service.get_by_average_rating(sort_by_rating=True, descending=True)


@recipe_router.get('/get_recipe/sort/average_rating/asc')
async def get_recipe_by_rate_asc(recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)]):
    return await recipe_service.get_by_average_rating(sort_by_rating=True)


@recipe_router.delete('/delete_recipe/')
async def delete_recipe(recipe_id: int,
                        recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)],
                        user: User = Depends(current_user)):
    return await recipe_service.delete_recipe(recipe_id)


@recipe_router.post('/create_recipe/')
async def create_recipe(
        recipe: RecipeCreate,
        recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)],
        user: User = Depends(current_user),
):
    await recipe_service.create_recipe(recipe)


@recipe_router.put('/update_recipe/')
async def update_recipe(
        recipe: RecipeCreate,
        recipe_id: int,
        recipe_service: Annotated[RecipeService, Depends(recipe_service_dp)],
        user: User = Depends(current_user)):
    return await recipe_service.update_recipe(recipe, recipe_id)


@recipe_router.put('/rate/{recipe_title}')
async def rate_recipe(recipe_title: str,
                      rating: int,
                      rating_service: Annotated[RatingService, Depends(rating_service_dp)],
                      user: User = Depends(current_user)):
    return await rating_service.create_rating(rating, user.id, recipe_title)
