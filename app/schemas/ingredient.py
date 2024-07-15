from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    name: str = Field(description='Название ингредиента', example='Помидоры')
    quantity: str = Field(description='Необходимое кол-во ингредиента', example='1кг.')

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Ингредиент: {self.name}, '
                f'Количество: {self.quantity}, '
                )


class IngredientRead(IngredientBase):
    id: int


class IngredientCreate(IngredientBase):
    pass
