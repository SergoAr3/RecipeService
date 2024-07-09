from fastapi import Depends
from googleapiclient.discovery import build
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_db
from app.repositories.rating import RatingRepository
from app.repositories.recipe import RecipeRepository
from app.services.google_drive.config import get_gd
from app.services.google_drive.google_drive import GoogleDriveService
from app.services.rating import RatingService
from app.services.recipe import RecipeService
from app.services.ingredient import IngredientService
from app.repositories.ingredient import IngredientRepository
from app.services.step import StepService
from app.repositories.step import StepRepository


def recipe_service_dp(db: AsyncSession = Depends(get_db)) -> RecipeService:
    recipe_repository = RecipeRepository(db)
    ingredient_repository = IngredientRepository(db)
    step_repository = StepRepository(db)
    rating_repository = RatingRepository(db)
    return RecipeService(recipe_repository, ingredient_repository, step_repository, rating_repository)


def ingredient_service_dp(db: AsyncSession = Depends(get_db)) -> IngredientService:
    repository = IngredientRepository(db)
    return IngredientService(repository)


def step_service_dp(db: AsyncSession = Depends(get_db)) -> StepService:
    repository = StepRepository(db)
    return StepService(repository)


def rating_service_dp(db: AsyncSession = Depends(get_db)) -> RatingService:
    recipe_repository = RecipeRepository(db)
    rating_repository = RatingRepository(db)
    return RatingService(rating_repository, recipe_repository)


def google_drive_service_dp(gd: build = Depends(get_gd)) -> GoogleDriveService:
    return GoogleDriveService(gd)

#
