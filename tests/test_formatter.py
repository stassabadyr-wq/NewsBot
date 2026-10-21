from src.formatter import format_article
from src.news_client import Article


def test_format_escapes_html():
    a = Article("A <b> & B", "x" * 300, "https://a.com/?q=1&r=2", "Src", "2026-10-21T00:00:00Z")
    text = format_article(a)
    assert "<b>A &lt;b&gt; &amp; B</b>" in text
    assert "..." in text
    assert 'href="https://a.com/?q=1&amp;r=2"' in text
