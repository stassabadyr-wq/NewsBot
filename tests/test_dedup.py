from src.dedup import SeenStore, select_new
from src.news_client import Article


def make(title, url):
    return Article(title, "", url, "test", "2026-10-21T00:00:00Z")


def test_url_and_title_dedup(tmp_path):
    store = SeenStore(str(tmp_path / "t.db"))
    first = make("OpenAI says its AI agents disabled monitoring", "https://a.com/x?utm=1")
    assert select_new([first], store) == [first]
    store.mark_sent(first)

    same_url = make("Другой заголовок про OpenAI", "https://a.com/x/")
    similar = make("OpenAI says its AI agents disabled their monitoring", "https://b.com/y")
    other = make("Python 3.14 released with new features", "https://c.com/z")
    assert select_new([same_url, similar, other], store) == [other]
