from fastapi import HTTPException

from app.repositories.rating import RatingRepository
from app.repositories.recipe import RecipeRepository
from app.schemas.rating import RatingRead


class RatingService:
    def __init__(self, rating_repository: RatingRepository, recipe_repository: RecipeRepository):
        self.rating_repository = rating_repository
        self.recipe_repository = recipe_repository

    async def get_rating_by_recipe_name(self, recipe_title: str) -> RatingRead:
        rating = await self.rating_repository.get(recipe_title=recipe_title)
        rating = RatingRead.from_orm(rating)
        return rating

    async def create_rating(self, user_rating: int, user_id: int, recipe_title: str) -> None:
        if user_rating > 5:
            raise HTTPException(status_code=400, detail="Оценка должна быть не выше 5!")
        await self.rating_repository.create(user_rating, user_id, recipe_title)

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
