from fastapi import Depends

import app.api.errors as err
from app.db import Rating
from app.repositories.rating import RatingRepository
from app.repositories.recipe import RecipeRepository
from app.schemas.rating import RatingRead


class RatingService:
    def __init__(self,
                 rating_repository: RatingRepository = Depends(),
                 recipe_repository: RecipeRepository = Depends()
                 ):
        self.rating_repository = rating_repository
        self.recipe_repository = recipe_repository

    async def get_rating_by_recipe_name(self, recipe_title: str) -> RatingRead:
        rating = await self.rating_repository.get(recipe_title=recipe_title)
        rating = RatingRead.from_orm(rating)
        return rating

    async def create_rating(self, user_rating: float, user_id: int, recipe_title: str) -> Rating | None:
        create_rating = await self.rating_repository.create(user_rating, user_id, recipe_title)
        if not create_rating:
            raise err.HTTP_404_NOT_FOUND_RECIPE

        ratings = await self.rating_repository.get(recipe_title=recipe_title)
        total = 0
        count = 0
        average_rating = 0
        for rating in ratings:
            total += rating.rating
            count += 1
        if count > 0:
            average_rating = total / count
        await self.recipe_repository.update_rating(recipe_title, average_rating)

        return create_rating
