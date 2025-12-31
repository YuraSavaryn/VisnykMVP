import asyncio
from sqlalchemy.pool import NullPool
from celery import chain
import datetime

from core.config import settings
from database import Database
from .celery_beat import celery_app
from .rss_parser import parse_rss
from services.news_service.news_core import (
    create_news_bulk,
    get_news_without_embedding,
    get_news_by_date,
    update_news_bulk,
)
from services.news_service.news_config import rss_channels, rss_urls
from services.ml_service.model_core import get_embedding, run_hdbscan_with_umap

worker_db_helper = Database(
    url=settings.db_url,
    poolclass=NullPool,
)


async def process_rss_async():
    async with worker_db_helper.session_factory() as session:
        for channel in rss_channels:
            channel_news = parse_rss(channel, rss_urls[channel])
            await create_news_bulk(session, channel_news)


async def process_news_embeddings():
    async with worker_db_helper.session_factory() as session:
        while True:
            news = await get_news_without_embedding(session=session, batch_size=32)
            if not news:
                return None
            titles = [item.title for item in news]
            embeddings = await get_embedding(titles)
            await update_news_bulk(
                session=session, news=news, feature="embedding", values=embeddings
            )


async def process_clusterization():
    certain_date = datetime.datetime.today()
    async with worker_db_helper.session_factory() as session:
        news = await get_news_by_date(session=session, certain_date=certain_date)
        embeddings = [n.embedding for n in news]
        labels = await run_hdbscan_with_umap(embeddings)
        await update_news_bulk(
            session=session, news=news, feature="cluster_id", values=labels
        )


@celery_app.task
def execute_parser_rss():
    asyncio.run(process_rss_async())


@celery_app.task
def add_news_embeddings(result=None):
    asyncio.run(process_news_embeddings())


@celery_app.task
def run_clusterization(result=None):
    asyncio.run(process_clusterization())


@celery_app.task
def run_full_parse_pipeline():
    pipeline = chain(execute_parser_rss.s(), add_news_embeddings.s())
    return pipeline()
