import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "").strip()
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "").strip()


def require(name: str, value: str) -> str:
    """Падаем с понятной ошибкой, если переменная не заполнена в .env."""
    if not value:
        raise RuntimeError(f"Переменная {name} не заполнена в файле .env")
    return value


# Поисковые запросы по языкам (синтаксис GNews: фразы в кавычках, OR между словами)
SEARCH_QUERIES = {
    "ru": '"искусственный интеллект" OR Python OR кибербезопасность OR OpenAI',
    "en": '"artificial intelligence" OR Python OR cybersecurity OR OpenAI',
}
MAX_ARTICLES_PER_REQUEST = 10

# Ключевые слова для фильтра (регистр не важен, ищем в заголовке и описании)
KEYWORDS = [
    "искусственный интеллект", "нейросет", "python", "кибербезопасност",
    "openai", "chatgpt", "artificial intelligence", "cybersecurity",
    "ai agent", "machine learning",
]
DB_PATH = "news.db"
SIMILARITY_THRESHOLD = 0.75  # 0..1, чем выше, тем строже считаем заголовки разными
DB_KEEP_DAYS = 30
