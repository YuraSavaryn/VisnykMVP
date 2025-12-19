import asyncio

from .celery_beat import celery_app
from .rss_parser import parse_rss
from services.news_service.news_core import create_news
from services.news_service.news_config import rss_channels, rss_urls
from database import db_helper


async def process_rss_async():
    async with db_helper.session_factory() as session:
        for channel in rss_channels:
            channel_news = parse_rss(channel, rss_urls[channel])

            for item in channel_news:
                await create_news(session, item)

        print("News are saved")


@celery_app.task
def execute_parser_rss():
    asyncio.run(process_rss_async())
