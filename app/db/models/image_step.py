from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class ImageStep(Base):
    __tablename__ = "image_step"
    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=True)
    step_id: Mapped[str] = mapped_column(ForeignKey('step.id', ondelete="CASCADE", onupdate="CASCADE"))

    step = relationship("Step", back_populates="image")
