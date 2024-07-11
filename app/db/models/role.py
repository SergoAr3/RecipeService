from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Role(Base):
    __tablename__ = "role_guide"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))

    user = relationship("User", back_populates="role")
