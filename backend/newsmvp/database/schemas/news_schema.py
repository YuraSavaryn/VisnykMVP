from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from .base import Base
from services.news_service.news_config import news_verification

if TYPE_CHECKING:
    from .news_source_schema import NewsSource
    from .news_type_schema import NewsType


class News(Base):
    __tablename__ = "news"

    news_source_id: Mapped[int] = mapped_column(ForeignKey("news_source.id"))
    news_type_id: Mapped[int] = mapped_column(ForeignKey("news_type.id"))
    title: Mapped[str]
    link: Mapped[str]
    summary: Mapped[str]
    published: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    news_verification: Mapped[str] = mapped_column(
        default=news_verification[0], server_default=news_verification[0]
    )
    embedding: Mapped[Vector] = mapped_column(Vector(384), nullable=True)
    cluster_id: Mapped[int] = mapped_column(server_default="-1")
    importance_level: Mapped[float] = mapped_column(server_default="0")

    news_source: Mapped["NewsSource"] = relationship(back_populates="news")
    news_type: Mapped["NewsType"] = relationship(back_populates="news")

    __table_args__ = (
        UniqueConstraint("news_source_id", "title", name="uq_news_source_title"),
    )
