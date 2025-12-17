from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from models import News, NewsCreate
from services.news_service import news_core

router = APIRouter(tags=["news"])


@router.get("/", response_model=list[News])
async def get_news(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await news_core.get_news(session)


@router.post("/", response_model=News)
async def create_news(
    news_in: NewsCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await news_core.create_news(session, news_in)


@router.get("/{news_id}/", response_model=News)
async def get_news_by_id(
    news_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    product = await news_core.get_news_by_id(session, news_id)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
