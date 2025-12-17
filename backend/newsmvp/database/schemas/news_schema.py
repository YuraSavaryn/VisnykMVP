from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class News(Base):
    __tablename__ = "news"

    source_name: Mapped[str]
    title: Mapped[str]
    link: Mapped[str]
    summary: Mapped[str]
    published: Mapped[datetime] = mapped_column(DateTime(timezone=True))
