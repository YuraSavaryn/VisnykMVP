from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.schemas import NewsType
from .news_config import types


async def create_base_news_type(session: AsyncSession):
    for example in types:
        session.add(NewsType(news_type=example))
    await session.commit()


async def get_news_type(
    session: AsyncSession,
    type_name: str,
) -> NewsType | None:
    stmt = select(NewsType).where(NewsType.news_type == type_name)
    news_type = await session.scalar(stmt)
    return news_type


async def get_news_type_id(session: AsyncSession, type_name: str) -> int:
    news_type = await get_news_type(session, type_name)

    if news_type is None:
        await create_base_news_type(session)
        news_type = await get_news_type(session, "unknown")
    return news_type.id
