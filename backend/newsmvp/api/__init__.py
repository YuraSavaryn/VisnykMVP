from fastapi import APIRouter

from .v1 import news_router

router_v1 = APIRouter()
router_v1.include_router(router=news_router, prefix="/news")
