import requests
import numpy as np
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from database import db_helper
from services.scrapper_service.news_text_parser import get_text_from_url
from services.news_service.news_core import (
    get_news_by_date,
    update_news_bulk,
)
from services.ml_service.model_core import (
    run_optics,
    run_hdbscan_with_umap,
    run_agglomerative,
)
from services.ml_service.evaluating_core import (
    evaluate_importance,
    evaluate_cluster_size,
)

router = APIRouter(tags=["model"])

data = {
    "model": "gemma2:2b",
    "stream": False,
    "keep_alive": "3m",
}

model_url = "http://localhost:11434/api/generate"


@router.get("/summarize")
async def send_summarize_prompt(article_url: str):
    prompt = """
    Ти професійний редакток, твоє завдання сумаризувати статті.
    Прочитай наступний текст новини і напиши короткий підсумок,
    де висвітлиш головну суть новини, пиши відповідь українською мовою (від 3 до 5 речень):
    """

    article_text = get_text_from_url(article_url)
    if article_text == "Error":
        return "Не вдалося прочитати вміст статті за посиланням!"
    prompt = prompt + article_text
    print(prompt)
    data["prompt"] = prompt

    response = requests.post(model_url, json=data)

    return response.json()["response"]


@router.get("/news_text")
async def get_news_text(article_url: str):
    article_text = get_text_from_url(article_url)
    return article_text


@router.post(
    "/cluster_news_hdbscan_with_umap", description="example of time: 2026-01-31"
)
async def cluster_news(
    certain_date: date,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    news = await get_news_by_date(session=session, certain_date=certain_date)
    embeddings = [n.embedding for n in news]
    labels = await run_hdbscan_with_umap(embeddings)
    await update_news_bulk(
        session=session, news=news, feature="cluster_id", values=labels
    )


@router.post("/cluster_news_optics", description="example of time: 2026-01-31")
async def cluster_news(
    certain_date: date,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    news = await get_news_by_date(session=session, certain_date=certain_date)
    embeddings = [n.embedding for n in news]
    labels = await run_optics(embeddings)
    await update_news_bulk(
        session=session, news=news, feature="cluster_id", values=labels
    )


@router.post("/cluster_news_aggloremative", description="example of time: 2026-01-31")
async def cluster_news(
    certain_date: date,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    news = await get_news_by_date(session=session, certain_date=certain_date)
    embeddings = [n.embedding for n in news]
    labels = await run_agglomerative(embeddings)
    await update_news_bulk(
        session=session, news=news, feature="cluster_id", values=labels
    )


@router.post("/cluster_news", description="example of time: 2026-01-31")
async def cluster_news(
    certain_date: date,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    methods = [
        run_hdbscan_with_umap,
        run_optics,
        run_agglomerative,
    ]
    news = await get_news_by_date(session=session, certain_date=certain_date)
    embeddings = [n.embedding for n in news]
    labels = []
    for method in methods:
        labels = await method(embeddings)
    await update_news_bulk(
        session=session, news=news, feature="cluster_id", values=labels
    )


@router.post("/evaluate_news_ner", description="example of time: 2026-01-31")
async def evaluate_news_ner(
    certain_date: date,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    news = await get_news_by_date(session=session, certain_date=certain_date)
    embeddings = np.array([n.embedding for n in news])

    labels = await run_optics(embeddings)

    await update_news_bulk(
        session=session, news=news, feature="cluster_id", values=labels
    )

    cluster_sizes = evaluate_cluster_size(labels)

    importance_levels = evaluate_importance(news, embeddings, labels, cluster_sizes)

    await update_news_bulk(
        session=session, news=news, feature="importance_level", values=importance_levels
    )
