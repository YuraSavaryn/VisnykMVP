from langchain_core.tools import tool
from ddgs import DDGS

from .news_retriever import NewsRetriever


@tool
def get_relevant_news(query: str) -> str:
    """search relevant news in local database"""
    retriever = NewsRetriever()
    # яка ситуація на фронті?
    results = retriever.invoke(query)

    if not results:
        return "У ЛОКАЛЬНІЙ БАЗІ ДАНИХ НІЧОГО НЕ ЗНАЙДЕНО. Спробуй скористатися пошуком в інтернеті або змінити запит."
    prompt = "Релевантна інформація:\n"
    for result in results:
        prompt += result.page_content + "\n"
    prompt += "Запит користувача: " + query
    return prompt


@tool
def search_in_web(query: str) -> str:
    """search news in web based on query"""
    ddgs = DDGS()

    try:
        results = ddgs.news(query, max_results=10)

        if not results:
            return f"Пошук у вебі за запитом '{query}' не дав результатів. Спробуй змінити ключові слова."
        return "\n".join(
            f"{result['source']} - {result['title']}: {result['body']}"
            for result in results
        )
    except Exception as e:
        return f"Помилка при пошуку в інтернеті: {str(e)}. Спробуй пізніше або використай локальну базу."


tools = [get_relevant_news, search_in_web]
