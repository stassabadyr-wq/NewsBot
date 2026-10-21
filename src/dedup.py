import re
import sqlite3
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from urllib.parse import urlsplit, urlunsplit

from src import config
from src.news_client import Article

SHORT_KEYWORDS = re.compile(r"\b(ai|ии|llm|gpt)\b", re.IGNORECASE)
EXTRA_KEYWORDS = ("кибератак",)
STOPWORDS = {
    "the", "and", "for", "with", "its", "their", "that", "this", "from", "about",
    "one", "even", "now", "will", "has", "have", "are", "was", "says", "said",
    "что", "как", "для", "над", "про", "при", "его", "это", "они", "или",
}


def normalize_url(url: str) -> str:
    """Убираем параметры отслеживания, фрагмент и хвостовой слэш."""
    parts = urlsplit(url.strip())
    path = parts.path.rstrip("/")
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, "", ""))


def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s]", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def tokens(normalized_title: str) -> set[str]:
    return {w for w in normalized_title.split() if len(w) > 2 and w not in STOPWORDS}


def titles_similar(a: str, b: str) -> bool:
    """a и b уже нормализованы."""
    if SequenceMatcher(None, a, b).ratio() >= config.SIMILARITY_THRESHOLD:
        return True
    ta, tb = tokens(a), tokens(b)
    smallest = min(len(ta), len(tb))
    if smallest < 4:
        return False
    return len(ta & tb) / smallest >= config.TOKEN_OVERLAP_THRESHOLD


def matches_keywords(article: Article) -> bool:
    title = article.title.lower()
    if any(kw in title for kw in config.KEYWORDS + list(EXTRA_KEYWORDS)):
        return True
    return bool(SHORT_KEYWORDS.search(article.title))


class SeenStore:
    def __init__(self, path: str = config.DB_PATH) -> None:
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS sent ("
            "url TEXT PRIMARY KEY, title TEXT NOT NULL, sent_at TEXT NOT NULL)"
        )
        self.conn.commit()

    def cleanup(self, days: int = config.DB_KEEP_DAYS) -> None:
        border = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        self.conn.execute("DELETE FROM sent WHERE sent_at < ?", (border,))
        self.conn.commit()

    def is_duplicate(self, article: Article) -> bool:
        url = normalize_url(article.url)
        if self.conn.execute("SELECT 1 FROM sent WHERE url = ?", (url,)).fetchone():
            return True
        new_title = normalize_title(article.title)
        for (old_title,) in self.conn.execute("SELECT title FROM sent"):
            if titles_similar(new_title, old_title):
                return True
        return False

    def mark_sent(self, article: Article) -> None:
        self.conn.execute(
            "INSERT OR IGNORE INTO sent (url, title, sent_at) VALUES (?, ?, ?)",
            (
                normalize_url(article.url),
                normalize_title(article.title),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()


def select_new(articles: list[Article], store: SeenStore) -> list[Article]:
    """Фильтр по ключевым словам + дубли (в том числе внутри самой пачки)."""
    result: list[Article] = []
    batch_titles: list[str] = []
    for a in articles:
        if not a.title or not a.url or not matches_keywords(a):
            continue
        if store.is_duplicate(a):
            continue
        title = normalize_title(a.title)
        if any(titles_similar(title, t) for t in batch_titles):
            continue
        batch_titles.append(title)
        result.append(a)
    return result
