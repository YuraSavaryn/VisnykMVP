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


class News(NewsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
