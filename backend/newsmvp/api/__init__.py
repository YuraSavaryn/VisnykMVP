from fastapi import APIRouter

from .v1 import news_router, news_source_router

router_v1 = APIRouter()
router_v1.include_router(router=news_router, prefix="/news")
router_v1.include_router(router=news_source_router, prefix="/news_source")
