from datetime import datetime
from sqlalchemy.orm import Mapped

from .base import Base


class News(Base):
    __tablename__ = "news"

    source_name: Mapped[str]
    title: Mapped[str]
    link: Mapped[str]
    summary: Mapped[str]
    published: Mapped[datetime]
