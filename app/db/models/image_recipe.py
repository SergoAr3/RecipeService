from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class ImageRecipe(Base):
    __tablename__ = "image_recipe"
    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=True)

    recipe = relationship("Recipe", back_populates="image")
