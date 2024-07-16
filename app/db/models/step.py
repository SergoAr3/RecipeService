import datetime

from sqlalchemy import ForeignKey, Interval, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Step(Base):
    __tablename__ = "step"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String(255))
    step_time: Mapped[datetime.timedelta] = mapped_column(Interval(), default=datetime.timedelta(seconds=0))
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id", ondelete="CASCADE"))

    recipe = relationship("Recipe", back_populates="steps")
