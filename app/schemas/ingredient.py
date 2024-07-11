from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    quantity: str

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Ингредиент: {self.name}, '
                f'Количество: {self.quantity}, '
                )


class IngredientRead(IngredientBase):
    id: int
    name: str
    quantity: str


class IngredientCreate(IngredientBase):
    pass
