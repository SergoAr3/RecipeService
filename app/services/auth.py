from fastapi import Depends

from app.auth.utils import hash_password
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    async def create_user_db(
            self,
            user_data: UserCreate,
    ):
        hashed_password = await hash_password(user_data.password)
        await self.user_repository.create(user_data.username, hashed_password)
