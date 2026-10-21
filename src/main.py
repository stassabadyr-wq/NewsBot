import argparse
import asyncio

from telegram import Bot
from telegram.error import RetryAfter, TelegramError

from src import config
from src.dedup import SeenStore, select_new
from src.formatter import build_text
from src.news_client import Article, NewsApiError, search_news


def collect() -> list[Article]:
    """Запрашиваем все языки; ошибка одного запроса не останавливает остальные."""
    articles: list[Article] = []
    for lang, query in config.SEARCH_QUERIES.items():
        try:
            articles.extend(search_news(query, lang, config.MAX_ARTICLES_PER_REQUEST))
        except NewsApiError as e:
            print(f"[{lang}] Ошибка: {e}")
    # Сначала самые свежие: при дублях останется более новая публикация
    articles.sort(key=lambda a: a.published_at, reverse=True)
    return articles


async def send_with_retry(bot: Bot, channel: str, text: str) -> None:
    try:
        await bot.send_message(chat_id=channel, text=text, parse_mode="HTML")
    except RetryAfter as e:
        delay = e.retry_after
        delay = delay.total_seconds() if hasattr(delay, "total_seconds") else delay
        await asyncio.sleep(delay + 1)
        await bot.send_message(chat_id=channel, text=text, parse_mode="HTML")


async def publish(items: list[Article], store: SeenStore) -> None:
    token = config.require("TELEGRAM_BOT_TOKEN", config.TELEGRAM_BOT_TOKEN)
    channel = config.require("TELEGRAM_CHANNEL_ID", config.TELEGRAM_CHANNEL_ID)
    sent = 0
    async with Bot(token) as bot:
        for a in items:
            try:
                text = await asyncio.to_thread(build_text, a)
                await send_with_retry(bot, channel, text)
            except TelegramError as e:
                # Не помечаем как отправленное: попробуем в следующий запуск
                print(f"Не отправлено ({a.title[:50]}...): {e}")
                continue
            store.mark_sent(a)
            sent += 1
            print(f"Отправлено: {a.title}")
            await asyncio.sleep(config.POST_DELAY_SECONDS)
    print(f"Итого отправлено: {sent}")


def main() -> None:
    parser = argparse.ArgumentParser(description="NewsBot")
    parser.add_argument("--dry-run", action="store_true",
                        help="показать, что было бы отправлено, ничего не публикуя")
    args = parser.parse_args()

    store = SeenStore()
    try:
        store.cleanup()
        fresh = select_new(collect(), store)[: config.MAX_POSTS_PER_RUN]
        print(f"К публикации: {len(fresh)}")
        if args.dry_run:
            for a in fresh:
                print(f"  * {a.source}: {a.title}")
            return
        if fresh:
            asyncio.run(publish(fresh, store))
    finally:
        store.close()


if __name__ == "__main__":
    main()

