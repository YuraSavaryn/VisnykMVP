from pydantic import BaseModel, ConfigDict
from datetime import datetime


class NewsBase(BaseModel):
    source_name: str
    title: str
    link: str
    summary: str
    published: datetime


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsCreate):
    pass


class NewsUpdatePartial(NewsCreate):
    source_name: str | None = None
    title: str | None = None
    link: str | None = None
    summary: str | None = None
    published: datetime | None = None


class News(NewsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
