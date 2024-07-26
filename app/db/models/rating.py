from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Rating(Base):
    __tablename__ = "rating"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rating: Mapped[float] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id", ondelete="CASCADE"), index=True)

    recipe = relationship("Recipe", back_populates="rating")
    user = relationship("User", back_populates="rating")

    __table_args__ = (UniqueConstraint('user_id', 'recipe_id', name='uniq_user_recipe'),)
