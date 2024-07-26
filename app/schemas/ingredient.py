from typing import Optional

from pydantic import Field

from app.schemas.config import ConfigBaseModel


class IngredientBase(ConfigBaseModel):
    name: str = Field(description='Название ингредиента', example='Помидоры')
    quantity: str = Field(description='Необходимое кол-во ингредиента', example='1кг.')

    def __str__(self):
        return (f'Ингредиент: {self.name}, '
                f'Количество: {self.quantity}, '
                )


class IngredientRead(IngredientBase):
    id: int


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    name: Optional[str] = None
    quantity: Optional[str] = None
