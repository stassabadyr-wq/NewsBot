from src.formatter import format_article
from src.news_client import Article
from src.translator import detect_lang


def test_detect_lang():
    assert detect_lang("Маск предупредил об угрозе ИИ") == "ru"
    assert detect_lang("OpenAI says its agents weakened monitoring") == "en"


def test_bilingual_format():
    a = Article("Заголовок", "Описание", "https://a.com/x", "Src", "2026-10-21T00:00:00Z")
    text = format_article(a, translation=("en", "Headline", "Description"), lang="ru")
    assert text.index("Заголовок") < text.index("Headline")
    assert "🇷🇺" in text and "🇬🇧" in text
