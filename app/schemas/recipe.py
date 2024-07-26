import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_serializer

from app.schemas.config import ConfigBaseModel
from app.schemas.ingredient import IngredientCreate
from app.schemas.step import StepCreate


class RecipeBase(ConfigBaseModel):
    title: str = Field(description='Название рецепта', example='Овощной салат')
    description: str = Field(description='Описание рецепта',
                             example='Это легкое и освежающее блюдо, состоящее из свежих овощей')
    ingredients: List[IngredientCreate] = Field(description='Список ингредиентов')
    steps: List[StepCreate] = Field(description='Шаги приготовления')


class RecipeRead(RecipeBase):
    id: int
    total_time: datetime.timedelta
    average_rating: float

    @field_serializer('total_time')
    @classmethod
    def serialize_total_time(cls, value):
        return str(value)

    def __str__(self):
        return (f'Блюдо: {self.title},\n'
                f'Описание: {self.description},\n '
                f'Время готовки: {str(self.total_time)},\n '
                f'Ингредиенты: {[str(ingredient) for ingredient in self.ingredients]},\n '
                f'Шаги приготовления: {[str(step) for step in self.steps]}\n\n'
                f'Средняя оценка: {self.average_rating}'
                )


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
