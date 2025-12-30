from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from database import db_helper
from models import News, NewsCreate, NewsUpdate, NewsUpdatePartial
from services.news_service import news_core
from .dependencies import news_by_id

router = APIRouter(tags=["news"])


@router.get("/{certain_date}/{batch_size}/", response_model=list[News])
async def get_news(
    certain_date: date = date(2026, 1, 31),
    batch_size: int = 20,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await news_core.get_news(session, certain_date, batch_size)


@router.get("/{news_id}/", response_model=News)
async def get_news_by_id(
    news: News = Depends(news_by_id),
) -> News:
    return news


@router.get("/worthy_news/{certain_date}/{batch_size}/", response_model=list[News])
async def get_worthy_news(
    certain_date: date,
    batch_size: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await news_core.get_worthy_news(session, certain_date, batch_size)


@router.post("/", response_model=News, status_code=status.HTTP_201_CREATED)
async def create_news(
    news_in: NewsCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await news_core.create_news(session, news_in)


@router.put("/{news_id}/")
async def update_news(
    news_update: NewsUpdate,
    news: News = Depends(news_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await news_core.update_news(
        session=session,
        news=news,
        news_update=news_update,
    )


@router.patch("/{news_id}/")
async def update_news_partial(
    news_update: NewsUpdatePartial,
    news: News = Depends(news_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await news_core.update_news(
        session=session,
        news=news,
        news_update=news_update,
        partial=True,
    )


@router.delete("/{news_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(
    news: News = Depends(news_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await news_core.delete_news(
        session=session,
        news=news,
    )
