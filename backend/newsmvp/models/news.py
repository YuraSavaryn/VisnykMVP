from pydantic import BaseModel, ConfigDict
from datetime import datetime


class NewsBase(BaseModel):
    news_source_id: int
    news_type_id: int
    title: str
    link: str
    summary: str
    published: datetime
    news_verification: str


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsCreate):
    pass


class NewsUpdatePartial(NewsCreate):
    news_source_id: int | None = None
    news_type_id: int | None = None
    title: str | None = None
    link: str | None = None
    summary: str | None = None
    published: datetime | None = None
    news_verification: str | None = None


class News(NewsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
