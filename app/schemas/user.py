from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    id: models.ID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    """
    username: str
    role_id: int


class UserCreate(schemas.BaseUserCreate):
    """
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    """
    username: str
