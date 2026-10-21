from html import escape

from src.news_client import Article


def format_article(a: Article) -> str:
    """Заголовок жирным, краткое описание, ссылка на источник (HTML для Telegram)."""
    parts = [f"<b>{escape(a.title)}</b>"]
    desc = a.description
    if len(desc) > 200:
        desc = desc[:197].rstrip() + "..."
    if desc:
        parts.append(escape(desc))
    source = escape(a.source or "Источник")
    parts.append(f'<a href="{escape(a.url, quote=True)}">{source}</a>')
    return "\n\n".join(parts)
