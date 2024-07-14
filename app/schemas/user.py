from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class UserRead(UserBase):
    id: int
    active: bool = True


class UserCreate(UserBase):
    pass
