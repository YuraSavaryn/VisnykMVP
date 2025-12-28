from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from models import News, NewsCreate, NewsUpdate, NewsUpdatePartial
from services.news_service import news_core
from .dependencies import news_by_id

router = APIRouter(tags=["news"])


# налаштувати отримання певної кількості новин та фільтрування за часом
@router.get("/", response_model=list[News])
async def get_news(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await news_core.get_news(session)


@router.post("/", response_model=News, status_code=status.HTTP_201_CREATED)
async def create_news(
    news_in: NewsCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await news_core.create_news(session, news_in)


@router.get("/{news_id}/", response_model=News)
async def get_news_by_id(
    news: News = Depends(news_by_id),
) -> News:
    return news


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
