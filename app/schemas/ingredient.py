from pydantic import BaseModel


class IngredientRead(BaseModel):
    id: int
    name: str
    quantity: str

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Ингредиент: {self.name}, '
                f'Количество: {self.quantity}, '
                )


class IngredientCreate(BaseModel):
    name: str
    quantity: str

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Ингредиент: {self.name}, '
                f'Количество: {self.quantity}, '
                )
