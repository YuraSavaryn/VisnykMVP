from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query

from models.news_source import NewsSource
from services.news_service import news_source_core
from database import db_helper

router = APIRouter(tags=["news_source"])


@router.get("/", response_model=list[NewsSource])
async def get_news_sources_by_id(
    ids: list[int] = Query(...),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    news_sources = await news_source_core.get_news_sources_by_id(session, ids)
    return news_sources
