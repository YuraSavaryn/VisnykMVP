import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics import (
    silhouette_score,  # від -1 до 1, 1 - ідеально, 0 - кластери накладуються, -1 - утворено кластери не вірно
    davies_bouldin_score,  # чим нижче, тим краще
    calinski_harabasz_score,  # чим вище, тим краще
)
import spacy
import csv

from .nlp_config import LOW_PRIORITY_KEYWORDS, weights

ner = spacy.load("uk_core_news_lg")
keyword_text = " ".join(LOW_PRIORITY_KEYWORDS)
keywords = ner(keyword_text)
keywords_lemmas = {token.lemma_.lower() for token in keywords}


async def evaluate_clusterization(algorithm, embeddings, labels):
    score_silhouette = silhouette_score(embeddings, labels)
    score_davies_bouldin = davies_bouldin_score(embeddings, labels)
    score_calinski_harabasz = calinski_harabasz_score(embeddings, labels)
    print(
        f"""{algorithm}
    \nsilhouette_score: {score_silhouette:.3f}
    \ndavies_bouldin_score: {score_davies_bouldin:.3f}
    \ncalinski_harabasz_score: {score_calinski_harabasz:.3f}"""
    )
    with open("metrics.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [algorithm, score_silhouette, score_davies_bouldin, score_calinski_harabasz]
        )


async def get_silhouette_score(embeddings, labels):
    score_silhouette = silhouette_score(embeddings, labels)
    return score_silhouette


def apply_topic_penalty(doc, current_score):
    found_lemmas = {token.lemma_.lower() for token in doc}

    if not found_lemmas.isdisjoint(keywords_lemmas):
        return 0.5
    return current_score


def evaluate_ner_importance(text, importance_score):
    doc = ner(text)

    for ent in doc.ents:
        importance_score += weights.get(ent.label_, 1)
    return apply_topic_penalty(doc, importance_score)


def evaluate_cluster_size(labels) -> dict:
    unique_labels, counts = np.unique(labels, return_counts=True)
    return dict(zip(unique_labels, counts))


def evaluate_importance(news, embeddings, labels, cluster_sizes):
    importance_levels = np.zeros(len(news))

    for cluster_id, size in cluster_sizes.items():
        cluster_indices = np.where(labels == cluster_id)[0]

        if size == 1:
            idx = cluster_indices[0]
            importance_levels[idx] = evaluate_ner_importance(news[idx].title, 1)
        elif cluster_id == -1:
            for i in cluster_indices:
                importance_levels[i] = evaluate_ner_importance(news[i].title, 1)
        else:
            cluster_vecs = embeddings[cluster_indices]
            centroid = np.mean(cluster_vecs, axis=0).reshape(1, -1)

            distances = cosine_distances(cluster_vecs, centroid).flatten()

            closest_local_idx = np.argmin(distances)
            target_idx = cluster_indices[closest_local_idx]

            importance_levels[target_idx] = evaluate_ner_importance(
                news[target_idx].title, int(size)
            )

    return importance_levels
