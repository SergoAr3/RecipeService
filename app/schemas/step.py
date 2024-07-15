import datetime

from pydantic import BaseModel, Field, field_validator, field_serializer


class StepBase(BaseModel):
    number: int = Field(description='Номер шага', example=1)
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

    class Config:
        from_attributes = True

    def __str__(self):
        return (f'Шаг {self.number}: '
                f'{self.description}'
                f'Длительность: {self.step_time}')


class StepRead(StepBase):
    id: int


class StepCreate(StepBase):

    @field_serializer('step_time')
    @classmethod
    def serialize_step_time(cls, value):
        return str(value)

# from enum import Enum
# from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
# from datetime import date, datetime
# from typing import Optional
# import re
#
#
# class Student(BaseModel):
#     student_id: int
#     phone_number: str = Field(default=..., description="Номер телефона в международном формате, начинающийся с '+'")
#     first_name: str = Field(default=..., min_length=1, max_length=50, description="Имя студента, от 1 до 50 символов")
#     last_name: str = Field(default=..., min_length=1, max_length=50,
#                            description="Фамилия студента, от 1 до 50 символов")
#     date_of_birth: date = Field(default=..., description="Дата рождения студента в формате ГГГГ-ММ-ДД")
#     email: EmailStr = Field(default=..., description="Электронная почта студента")
#     address: str = Field(default=..., min_length=10, max_length=200,
#                          description="Адрес студента, не более 200 символов")
#     enrollment_year: int = Field(default=..., ge=2002, description="Год поступления должен быть не меньше 2002")
#     major: Major = Field(default=..., description="Специальность студента")
#     course: int = Field(default=..., ge=1, le=5, description="Курс должен быть в диапазоне от 1 до 5")
#     special_notes: Optional[str] = Field(default=None, max_length=500,
#                                          description="Дополнительные заметки, не более 500 символов")
#
#     @field_validator("phone_number")
#     @classmethod
#     def validate_phone_number(cls, values: str) -> str:
#         if not re.match(r'^\+\d{1,15}$', values):
#             raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
#         return values
#
#     @field_validator("date_of_birth")
#     @classmethod
#     def validate_date_of_birth(cls, values: date):
#         if values and values >= datetime.now().date():
#             raise ValueError('Дата рождения должна быть в прошлом')
#         return values
