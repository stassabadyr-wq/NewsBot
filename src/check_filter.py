from src import config
from src.dedup import SeenStore, select_new
from src.news_client import NewsApiError, search_news


def main() -> None:
    store = SeenStore()
    for lang, query in config.SEARCH_QUERIES.items():
        try:
            articles = search_news(query, lang, config.MAX_ARTICLES_PER_REQUEST)
        except NewsApiError as e:
            print(f"[{lang}] Ошибка: {e}")
            continue
        fresh = select_new(articles, store)
        print(f"[{lang}] получено {len(articles)}, после фильтра и дублей: {len(fresh)}")
        for a in fresh:
            print(f"  + {a.source}: {a.title}")
    store.close()


if __name__ == "__main__":
    main()
