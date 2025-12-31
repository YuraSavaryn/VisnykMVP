import httpx
import hdbscan
from sklearn.cluster import OPTICS, AgglomerativeClustering
import umap

from .evaluating_core import evaluate_clusterization, get_silhouette_score


async def get_embedding(titles) -> list[list[float]]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8082/embed",  # "http://127.0.0.1:8082/embed",  "http://encoder:80/embed",
            json={"inputs": titles},
        )
        return response.json()


async def reduce_embeddings(embeddings):
    reducer = umap.UMAP(
        n_neighbors=15,
        n_components=10,
        metric="cosine",
        min_dist=0.0,
        random_state=42,
    )
    reduced_embeddings = reducer.fit_transform(embeddings)
    return reduced_embeddings


async def run_hdbscan_with_umap(embeddings):
    reduced_embeddings = await reduce_embeddings(embeddings)
    news_scaner = hdbscan.HDBSCAN(
        min_cluster_size=3,
        cluster_selection_method="leaf",
        cluster_selection_epsilon=0.1,
        gen_min_span_tree=True,
    )
    labels = news_scaner.fit_predict(reduced_embeddings)
    await evaluate_clusterization("HDBSCAN + UMAP", reduced_embeddings, labels)
    return labels


async def run_optics(embeddings):
    reduced_embeddings = await reduce_embeddings(embeddings)
    news_scaner = OPTICS(
        metric="euclidean",
        min_samples=2,
        min_cluster_size=2,
        cluster_method="xi",
        xi=0.003,
    ).fit(reduced_embeddings)
    await evaluate_clusterization("OPTICS", reduced_embeddings, news_scaner.labels_)
    return news_scaner.labels_


async def run_agglomerative(embeddings):
    start = round(len(embeddings) * 0.3)
    end = round(len(embeddings) * 0.7)
    score = -1
    labels = []
    top_n = 0
    for n in range(start, end):
        news_scaner = AgglomerativeClustering(
            metric="cosine",
            linkage="average",
            n_clusters=n,
        ).fit(embeddings)
        new_score = await get_silhouette_score(embeddings, news_scaner.labels_)
        if new_score > score:
            score = new_score
            labels.append(news_scaner.labels_)
            top_n = n
    print(top_n)
    await evaluate_clusterization("Agglomerative", embeddings, labels[-1])
    return labels[-1]
