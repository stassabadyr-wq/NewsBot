import re

from deep_translator import GoogleTranslator, MyMemoryTranslator

from src import config

CYRILLIC = re.compile(r"[а-яёА-ЯЁ]")
MYMEMORY_CODES = {"ru": "ru-RU", "en": "en-GB"}


def detect_lang(text: str) -> str:
    """'ru', если в тексте много кириллицы, иначе 'en'."""
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "en"
    cyr = sum(1 for c in letters if CYRILLIC.match(c))
    return "ru" if cyr / len(letters) > 0.3 else "en"


def _google(text: str, source: str, target: str) -> str:
    return GoogleTranslator(source=source, target=target).translate(text) or ""


def _mymemory(text: str, source: str, target: str) -> str:
    kwargs = {"email": config.MYMEMORY_EMAIL} if config.MYMEMORY_EMAIL else {}
    result = MyMemoryTranslator(
        source=MYMEMORY_CODES[source], target=MYMEMORY_CODES[target], **kwargs
    ).translate(text) or ""
    if result.upper().startswith("MYMEMORY WARNING"):
        return ""
    return result


def translate(text: str, target: str) -> str:
    """Перевод на target ('ru' или 'en'). Пробуем Google, затем MyMemory.
    При неудаче возвращает пустую строку (пост уйдёт без перевода)."""
    if not text:
        return ""
    source = "en" if target == "ru" else "ru"
    for engine in (_google, _mymemory):
        try:
            result = engine(text, source, target).strip()
            if result:
                return result
        except Exception as e:
            print(f"Перевод ({engine.__name__}) не удался: {type(e).__name__}")
    return ""
