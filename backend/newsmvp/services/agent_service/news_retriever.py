from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List
from sqlalchemy import text

from .agent_config import embeddings, vector_store


class NewsRetriever(BaseRetriever):
    def _get_relevant_documents(self, query: str) -> List[Document]:
        query_vector = embeddings.embed_query(query)

        with vector_store._engine.connect() as conn:
            sql = text(
                """
                SELECT title, 1 - (embedding <=> CAST(:vec AS vector)) as similarity
                FROM news
                ORDER BY embedding <=> CAST(:vec AS vector)
                LIMIT :k
            """
            )
            relevant_news = conn.execute(sql, {"vec": str(query_vector), "k": 5})
            results = []
            for result in relevant_news:
                results.append(Document(page_content=result.title))
            return results
