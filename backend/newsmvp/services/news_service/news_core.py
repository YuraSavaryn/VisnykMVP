from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from database.schemas import News
from models import NewsCreate, NewsUpdate, NewsUpdatePartial


async def get_news(session: AsyncSession) -> list[News]:
    stmt = select(News).order_by(News.published)
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
