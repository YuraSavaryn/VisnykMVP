from typing import TYPE_CHECKING
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .news_schema import News


class NewsType(Base):
    __tablename__ = "news_type"

    news_type: Mapped[str] = mapped_column(unique=True)
    type_embedding: Mapped[Vector] = mapped_column(Vector(384), nullable=True)

    news: Mapped[list["News"]] = relationship(back_populates="news_type")
