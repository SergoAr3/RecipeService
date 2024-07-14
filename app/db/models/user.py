from sqlalchemy import String, LargeBinary, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64))
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    rating = relationship("Rating", back_populates="user")
