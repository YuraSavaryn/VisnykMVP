from pydantic import BaseModel, ConfigDict


class NewsSourceBase(BaseModel):
    source_title: str
    fake_news_count: int
    is_blacklisted: bool


class NewsSource(NewsSourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
