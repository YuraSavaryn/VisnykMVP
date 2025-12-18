from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from database.schemas import News
from services.news_service import news_core


async def news_by_id(
    news_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> News:
    product = await news_core.get_news_by_id(session, news_id)
    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="News not found",
    )
