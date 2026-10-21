from html import escape

from src.news_client import Article
from src.translator import detect_lang, translate

FLAGS = {"ru": "🇷🇺", "en": "🇬🇧"}


def _short(desc: str) -> str:
    if len(desc) > 200:
        desc = desc[:197].rstrip() + "..."
    return desc


def format_article(a: Article, translation=None, lang: str | None = None) -> str:
    """Заголовок жирным, описание, ссылка (HTML для Telegram).

    translation = (язык_перевода, заголовок, описание); lang = язык оригинала.
    """
    desc = _short(a.description)
    link = f'<a href="{escape(a.url, quote=True)}">{escape(a.source or "Источник")}</a>'

    if translation is None:
        parts = [f"<b>{escape(a.title)}</b>"]
        if desc:
            parts.append(escape(desc))
        parts.append(link)
        return "\n\n".join(parts)

    t_lang, t_title, t_desc = translation
    parts = [f"{FLAGS[lang]} <b>{escape(a.title)}</b>"]
    if desc:
        parts.append(escape(desc))
    parts.append(f"{FLAGS[t_lang]} <b>{escape(t_title)}</b>")
    if t_desc:
        parts.append(escape(t_desc))
    parts.append(link)
    return "\n\n".join(parts)


def build_text(a: Article) -> str:
    """Оригинал + перевод на другой язык. Если перевод не удался, только оригинал."""
    lang = detect_lang(a.title)
    target = "en" if lang == "ru" else "ru"
    t_title = translate(a.title, target)
    if not t_title:
        return format_article(a)
    t_desc = translate(_short(a.description), target)
    return format_article(a, translation=(target, t_title, t_desc), lang=lang)
