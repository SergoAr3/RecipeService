from pydantic import BaseModel


class RatingRead(BaseModel):
    id: int
    rating: float
    user_id: str
    recipe_id: int

    class Config:
        from_attributes = True

    # def __str__(self):
    #     return (f'Шаг {self.number}: '
    #             f'{self.description}'
    #             f'Длительность: {self.step_time}')


class RatingCreate(BaseModel):
    rating: float

    class Config:
        from_attributes = True

    # def __str__(self):
    #     return (f'Шаг {self.number}: '
    #             f'{self.description}'
    #             f'Длительность: {self.step_time}')
