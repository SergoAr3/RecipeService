import datetime
from typing import Optional

from pydantic import Field, field_serializer, field_validator

from app.schemas.config import ConfigBaseModel


class StepBase(ConfigBaseModel):
    description: str = Field(description='Описание шага', example='Порезать мелко овощи')
    step_time: datetime.timedelta = Field(description='Длительность шага в формате HH:MM:SS',
                                          example=datetime.time(minute=10))

    @field_validator('step_time', mode='before')
    @classmethod
    def validate_step_time(cls, value):
        if isinstance(value, str):
            value = datetime.datetime.strptime(value, '%H:%M:%S').time()
            return datetime.timedelta(hours=value.hour, minutes=value.minute, seconds=value.second)
        else:
            return value

    def __str__(self):
        return (f'Шаг {self.number}: '
                f'{self.description}'
                f'Длительность: {self.step_time}')


class StepRead(StepBase):
    id: int
    number: int = Field(description='Номер шага', example=1)


class StepCreate(StepBase):
    number: int = Field(description='Номер шага', example=1)

    @field_serializer('step_time')
    @classmethod
    def serialize_step_time(cls, value):
        return str(value)


class StepUpdate(StepBase):
    description: Optional[str] = None
    step_time: Optional[datetime.timedelta] = None
