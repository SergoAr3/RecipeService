import datetime

from sqlalchemy import ForeignKey, Interval, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Recipe(Base):
    __tablename__ = "recipe"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100))
    total_time: Mapped[datetime.timedelta] = mapped_column(Interval(), default=datetime.timedelta(seconds=0),
                                                           index=True)
    average_rating: Mapped[float] = mapped_column(default=0.0, index=True)
    image_id: Mapped[str] = mapped_column(ForeignKey('image_recipe.id', ondelete="SET NULL", onupdate='CASCADE'),
                                          index=True, nullable=True)

    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan", lazy="selectin")
    steps = relationship("Step", back_populates="recipe", cascade="all, delete-orphan", lazy="selectin")
    rating = relationship("Rating", back_populates="recipe", lazy="selectin")
    image = relationship("ImageRecipe", back_populates="recipe", lazy="selectin")
