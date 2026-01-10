from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.schemas import NewsType
from .news_config import types_new
from services.ml_service.model_core import get_embedding


async def create_base_news_type(session: AsyncSession):
    for key in types_new.keys():
        embedding = await get_embedding(types_new[key])
        embedding = embedding[0] if isinstance(embedding[0], list) else embedding
        session.add(NewsType(news_type=key, type_embedding=embedding))
    await session.commit()


async def get_news_type(
    session: AsyncSession,
    type_name: str,
) -> NewsType:
    stmt = select(NewsType).where(NewsType.news_type == type_name)
    news_type = await session.scalar(stmt)
    return news_type


async def get_news_type_id(session: AsyncSession, type_name: str) -> int:
    news_type = await get_news_type(session, type_name)

    if news_type is None:
        await create_base_news_type(session)
        news_type = await get_news_type(session, "unknown")
    return news_type.id
