import time
from dataclasses import dataclass

import requests

from src import config

GNEWS_URL = "https://gnews.io/api/v4/search"
MIN_INTERVAL = 1.2  # минимум секунд между запросами (лимит GNews ~1 запрос/сек)
RETRY_DELAYS = (2, 5)  # паузы перед повтором при ошибке 429

_last_call = 0.0


class NewsApiError(Exception):
    """Ошибка API новостей (без ключа в тексте)."""


@dataclass(frozen=True)
class Article:
    title: str
    description: str
    url: str
    source: str
    published_at: str


def _throttle() -> None:
    global _last_call
    wait = MIN_INTERVAL - (time.monotonic() - _last_call)
    if wait > 0:
        time.sleep(wait)
    _last_call = time.monotonic()


def search_news(query: str, lang: str, max_results: int = 10) -> list[Article]:
    api_key = config.require("NEWS_API_KEY", config.NEWS_API_KEY)
    params = {
        "q": query,
        "lang": lang,
        "max": max_results,
        "sortby": "publishedAt",
        "apikey": api_key,
    }

    for attempt in range(len(RETRY_DELAYS) + 1):
        _throttle()
        try:
            response = requests.get(GNEWS_URL, params=params, timeout=15)
        except requests.RequestException as e:
            # Не выводим сам объект ошибки: в нём может быть URL с ключом
            raise NewsApiError(f"Сеть недоступна ({type(e).__name__})") from None
        if response.status_code == 429 and attempt < len(RETRY_DELAYS):
            time.sleep(RETRY_DELAYS[attempt])
            continue
        break

    if response.status_code != 200:
        raise NewsApiError(f"GNews вернул {response.status_code}: {response.text[:200]}")

    data = response.json()
    articles = []
    for item in data.get("articles", []):
        articles.append(
            Article(
                title=(item.get("title") or "").strip(),
                description=(item.get("description") or "").strip(),
                url=(item.get("url") or "").strip(),
                source=((item.get("source") or {}).get("name") or "").strip(),
                published_at=item.get("publishedAt") or "",
            )
        )
    return articles
