import datetime
from typing import List

from pydantic import BaseModel, field_serializer

from app.schemas.ingredient import IngredientCreate
from app.schemas.step import StepCreate


class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: List[IngredientCreate]
    steps: List[StepCreate]

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Блюдо: {self.title},\n'
                f'Описание: {self.description},\n '
                f'Время готовки: {str(self.total_time)},\n '
                f'Ингредиенты: {[str(ingredient) for ingredient in self.ingredients]},\n '
                f'Шаги приготовления: {[str(step) for step in self.steps]}\n\n'
                f'Средняя оценка: {self.average_rating}'
                f'Фото: {self.image_url}'
                )


class RecipeRead(RecipeBase):
    id: int
    total_time: datetime.timedelta
    average_rating: float
    image_url: str | None

    @field_serializer('total_time')
    @classmethod
    def serialize_total_time(cls, value):
        return str(value)


class RecipeCreate(RecipeBase):
    pass
