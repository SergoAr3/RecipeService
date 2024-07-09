from pydantic import BaseModel


class StepRead(BaseModel):
    id: int
    number: int
    description: str
    step_time: int

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Шаг {self.number}: '
                f'{self.description}'
                f'Длительность: {self.step_time}')


class StepCreate(BaseModel):
    number: int
    description: str
    step_time: int

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Шаг {self.number}: '
                f'{self.description}'
                f'Длительность: {self.step_time}')
