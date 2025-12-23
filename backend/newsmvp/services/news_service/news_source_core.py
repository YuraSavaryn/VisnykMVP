from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.schemas import NewsSource


async def create_news_source(session: AsyncSession, source_title) -> NewsSource:
    news_source = NewsSource(source_title=source_title)
    session.add(news_source)
    await session.commit()
    return news_source


async def get_news_source_by_title(
    session: AsyncSession,
    source_title: str,
) -> NewsSource | None:
    stmt = select(NewsSource).where(NewsSource.source_title == source_title)
    news_source = await session.scalar(stmt)
    return news_source


async def get_news_source_id(session: AsyncSession, source_title: str) -> int:
    news_source = await get_news_source_by_title(session, source_title)

    if news_source is None:
        news_source = await create_news_source(session, source_title)
    return news_source.id
