from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_postgres import PGVector
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT = """Ти — професійний аналітик новин. Твоя мета — надати максимально повну відповідь.

ПРАВИЛА РОБОТИ:
1. Спочатку ЗАВЖДИ шукай у локальній базі (get_relevant_news).
2. ПЕРЕВІРКА: Оціни отримані дані. Якщо в базі знайдено менше 3-х релевантних новин або інформація здається застарілою,
 ти ЗОБОВ'ЯЗАНИЙ використати пошук у браузері (search_in_web).
3. ПОРІВНЯННЯ: Якщо дані з бази та вебу різняться, обов'язково вкажи на ці розбіжності.
4. ЦИКЛ: Ти можеш викликати інструменти кілька разів з різними запитами, якщо перша спроба була невдалою.
5. ФІНАЛЬНИЙ АНАЛІЗ: Не просто цитуй новини, а зроби короткий висновок: як ситуація змінилася з часом.
 Якщо немає даних новин у базі даних та пошук теж не дав жодних результатів, скажи що не володієш інформацією
 на цю тему."""

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
)

connection = os.getenv("RAG_URL")
collection_name = "news"

embeddings = HuggingFaceEndpointEmbeddings(
    model="http://127.0.0.1:8082/embed",
)

vector_store = PGVector(
    embeddings=embeddings,
    connection=connection,
    collection_name=collection_name,
    use_jsonb=True,
)
