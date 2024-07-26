from pydantic import field_validator

from app.schemas.config import ConfigBaseModel


class RatingBase(ConfigBaseModel):
    rating: float

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, value: float):
        if not value or value < 1 or value > 5:
            raise ValueError('Оценка должна быть от 1 до 5!')
        return value


class RatingRead(RatingBase):
    id: int
    rating: float
    user_id: str
    recipe_id: int


class RatingCreate(RatingBase):
    pass
