from pydantic import BaseModel, field_validator


class RatingBase(BaseModel):
    rating: float

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, value: float):
        if not value or value < 1 or value > 5:
            raise ValueError('Оценка должна быть от 1 до 5!')
        return value

    class Config:
        from_attributes = True


class RatingRead(RatingBase):
    id: int
    rating: float
    user_id: str
    recipe_id: int

    class Config:
        from_attributes = True


class RatingCreate(RatingBase):
    pass
