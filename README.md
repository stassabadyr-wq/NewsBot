# NewsBot

Telegram-бот на Python: сам ищет свежие новости по ключевым словам через GNews API, отсеивает нерелевантные и дублирующиеся материалы и публикует остальное в Telegram-канал.

## Возможности

- поиск новостей на русском и английском через GNews API (паузы и повтор при лимите частоты);
- фильтр по ключевым словам в заголовке;
- защита от дублей: по ссылке и по похожести заголовков (SQLite);
- публикация в канал с HTML-оформлением и лимитом сообщений за запуск;
- режим --dry-run без публикации;
- запуск по расписанию (Планировщик заданий Windows).

## Установка

    git clone https://github.com/stassabadyr-wq/NewsBot.git
    cd NewsBot
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Copy-Item .env.example .env

Заполните файл .env:

    TELEGRAM_BOT_TOKEN=токен от @BotFather
    TELEGRAM_CHANNEL_ID=@username_канала
    NEWS_API_KEY=ключ с gnews.io

Бот должен быть администратором канала с правом публикации сообщений.

## Запуск

    python -m src.main --dry-run   # показать, что будет отправлено
    python -m src.main             # опубликовать
    python -m pytest -q            # тесты

Ключевые слова, поисковые запросы и лимиты настраиваются в src/config.py.

## Структура

- src/news_client.py - запросы к GNews
- src/dedup.py - фильтр и защита от дублей
- src/formatter.py - оформление сообщений
- src/main.py - главный сценарий
- run.ps1 - запуск для Планировщика заданий

## Автор

Stanislav Sabadyr
