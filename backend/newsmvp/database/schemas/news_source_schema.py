from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .news_schema import News


class NewsSource(Base):
    __tablename__ = "news_source"

    source_title: Mapped[str] = mapped_column(unique=True)
    fake_news_count: Mapped[int] = mapped_column(default=0, server_default="0")
    is_blacklisted: Mapped[bool] = mapped_column(default=False, server_default="false")

    news: Mapped[list["News"]] = relationship(back_populates="news_source")
