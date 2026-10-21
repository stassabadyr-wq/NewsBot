import re

from deep_translator import GoogleTranslator

CYRILLIC = re.compile(r"[а-яёА-ЯЁ]")


def detect_lang(text: str) -> str:
    """'ru', если в тексте много кириллицы, иначе 'en'."""
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "en"
    cyr = sum(1 for c in letters if CYRILLIC.match(c))
    return "ru" if cyr / len(letters) > 0.3 else "en"


def translate(text: str, target: str) -> str:
    """Перевод на target ('ru' или 'en'). При любой ошибке возвращает пустую строку."""
    if not text:
        return ""
    try:
        return (GoogleTranslator(source="auto", target=target).translate(text) or "").strip()
    except Exception:
        return ""
