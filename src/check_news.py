from src import config
from src.news_client import NewsApiError, search_news


def main() -> None:
    for lang, query in config.SEARCH_QUERIES.items():
        print(f"\n=== Язык: {lang} | Запрос: {query} ===")
        try:
            articles = search_news(query, lang, config.MAX_ARTICLES_PER_REQUEST)
        except NewsApiError as e:
            print(f"Ошибка: {e}")
            continue
        print(f"Найдено статей: {len(articles)}")
        for a in articles[:5]:
            print(f"- [{a.published_at}] {a.source}: {a.title}")
            print(f"  {a.url}")


if __name__ == "__main__":
    main()
