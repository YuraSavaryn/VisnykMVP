from sqlalchemy import select, desc
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from database.schemas import News
from models import NewsCreate, NewsUpdate, NewsUpdatePartial
from .news_source_core import get_news_source_id
from .news_type_core import get_news_type_id


async def get_news(session: AsyncSession) -> list[News]:
    stmt = select(News).order_by(desc(News.published))
    result: Result = await session.execute(stmt)
    news = result.scalars().all()
    return list(news)


async def get_news_by_id(session: AsyncSession, news_id: int) -> News | None:
    return await session.get(News, news_id)


async def create_news(session: AsyncSession, news_in: NewsCreate) -> News:
    product = News(**news_in.model_dump())
    session.add(product)
    await session.commit()
    return product


async def create_news_bulk(session: AsyncSession, news_values: list[dict]) -> None:
    if news_values is None:
        return None

    source_id = await get_news_source_id(session, news_values[0]["source_title"])
    type_id = await get_news_type_id(session, news_values[0]["news_type"])
    news_in = [
        {
            "news_source_id": source_id,
            "news_type_id": type_id,
            "title": news["title"],
            "link": news["link"],
            "summary": news["summary"],
            "published": news["published"],
            "news_verification": news["news_verification"],
        }
        for news in news_values
    ]

    stmt = pg_insert(News).values(news_in)
    await session.execute(stmt)
    await session.commit()


async def update_news(
    session: AsyncSession,
    news: News,
    news_update: NewsUpdate | NewsUpdatePartial,
    partial: bool = False,
) -> News:
    for name, value in news_update.model_dump(exclude_unset=partial).items():
        setattr(news, name, value)
    await session.commit()
    return news


async def delete_news(session: AsyncSession, news: News) -> None:
    await session.delete(news)
    await session.commit()
