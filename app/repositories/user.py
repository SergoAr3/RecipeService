from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User
from app.db.db import get_db


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, username: str) -> User | None:
        user = await self.db.execute(select(User).where(User.username == username))
        user = user.scalar()
        return user

    async def create(self, username: str, hashed_password: bytes) -> None | User:
        user = await self.get(username)
        if user is None:
            user = User(
                username=username,
                hashed_password=hashed_password
            )
            self.db.add(user)
            return
        return user
