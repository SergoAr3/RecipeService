from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


# from schemas.tasks import TaskSchema


class Recipe(Base):
    __tablename__ = "recipe"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100))
    total_time: Mapped[int] = mapped_column(default=0)
    average_rating: Mapped[float] = mapped_column(default=0.0)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)

    ingredient = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")
    step = relationship("Step", back_populates="recipe", cascade="all, delete-orphan")
    rating = relationship("Rating", back_populates="recipe")
