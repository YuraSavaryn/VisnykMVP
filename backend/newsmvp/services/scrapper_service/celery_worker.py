import asyncio
from sqlalchemy.pool import NullPool

from core.config import settings
from .celery_beat import celery_app
from .rss_parser import parse_rss
from services.news_service.news_core import create_news_bulk
from services.news_service.news_config import rss_channels, rss_urls
from database import Database


async def process_rss_async():
    worker_db_helper = Database(
        url=settings.db_url,
        poolclass=NullPool,
    )

    async with worker_db_helper.session_factory() as session:
        for channel in rss_channels:
            channel_news = parse_rss(channel, rss_urls[channel])
            await create_news_bulk(session, channel_news)

        print("News are saved")


@celery_app.task
def execute_parser_rss():
    asyncio.run(process_rss_async())
