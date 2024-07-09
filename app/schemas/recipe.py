from typing import List

from pydantic import BaseModel

from app.schemas.ingredient import IngredientCreate
from app.schemas.step import StepCreate


class RecipeRead(BaseModel):
    id: int
    title: str
    description: str
    total_time: int
    average_rating: float
    ingredients: List[IngredientCreate]
    steps: List[StepCreate]
    image_url: str | None

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Блюдо: {self.title},\n'
                f'Описание: {self.description},\n '
                f'Время готовки: {self.total_time},\n '
                f'Ингредиенты: {[str(ingredient) for ingredient in self.ingredients]},\n '
                f'Шаги приготовления: {[str(step) for step in self.steps]}\n\n'
                f'Средняя оценка: {self.average_rating}'
                f'Фото: {self.image_url}'
                )


class RecipeCreate(BaseModel):
    title: str
    description: str
    ingredients: List[IngredientCreate]
    steps: List[StepCreate]

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Блюдо: {self.title},\n'
                f'Описание: {self.description},\n '
                f'Время готовки: {self.total_time},\n '
                f'Ингредиенты: {[str(ingredient) for ingredient in self.ingredients]},\n '
                f'Шаги приготовления: {[str(step) for step in self.steps]}\n\n'
                f'Средняя оценка: {self.average_rating}')
