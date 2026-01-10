from typing import Any
from sqlalchemy import select, update, desc
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from datetime import timedelta, date

from database.schemas import News
from models import NewsCreate, NewsUpdate, NewsUpdatePartial
from .news_source_core import get_news_source_id
from .news_type_core import get_news_type_id


async def get_news(
    session: AsyncSession,
    certain_date: date = "2026-01-31",
    batch_size: int = 20,
) -> list[News]:
    start_of_day = certain_date
    end_of_day = start_of_day + timedelta(days=1)

    stmt = (
        select(News)
        .where(News.published >= start_of_day)
        .where(News.published < end_of_day)
        .order_by(desc(News.published))
        .limit(batch_size)
    )
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_news_by_id(
    session: AsyncSession,
    news_id: int,
) -> News | None:
    return await session.get(News, news_id)


async def get_news_without_embedding(
    session: AsyncSession,
    batch_size: int = 32,
) -> list[News] | None:
    stmt = (
        select(News)
        .where(News.embedding == None)
        .limit(batch_size)
        .with_for_update(skip_locked=True)
    )
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_news_by_date(
    session: AsyncSession,
    certain_date: date,
) -> list[News]:
    start_of_day = certain_date
    end_of_day = start_of_day + timedelta(days=1)

    stmt = (
        select(News)
        .where(News.published >= start_of_day)
        .where(News.published < end_of_day)
        .order_by(desc(News.published))
    )

    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_news_by_category(
    session: AsyncSession,
    certain_date: date,
    category_embedding: list,
    batch_size: int = 20,
):
    start_of_day = certain_date
    end_of_day = start_of_day + timedelta(days=1)
    distance_func = News.embedding.cosine_distance(category_embedding)
    threshold = 0.7

    stmt = (
        select(News)
        .where(News.published >= start_of_day)
        .where(News.published < end_of_day)
        .where(distance_func < threshold)
        .order_by(distance_func)
        .limit(batch_size)
    )

    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_worthy_news(
    session: AsyncSession,
    certain_date: date,
    batch_size: int = 20,
) -> list[News]:
    start = certain_date
    end = start + timedelta(days=1)

    stmt = (
        select(News)
        .where(News.published >= start, News.published < end)
        .order_by(desc(News.importance_level))
        .limit(batch_size)
    )
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_all_news(session: AsyncSession) -> list[News]:
    stmt = select(News)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


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
            "embedding": None,
            "cluster_id": -2,
            "importance_level": 0,
        }
        for news in news_values
    ]

    stmt = pg_insert(News).values(news_in)
    stmt = stmt.on_conflict_do_nothing(index_elements=["news_source_id", "title"])

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


async def update_news_bulk(
    session: AsyncSession,
    news: list[News],
    feature: str,
    values: Any,
):
    updated_data = [
        {"id": item.id, feature: value} for item, value in zip(news, values)
    ]
    await session.execute(update(News), updated_data)
    await session.commit()


async def delete_news(session: AsyncSession, news: News) -> None:
    await session.delete(news)
    await session.commit()
