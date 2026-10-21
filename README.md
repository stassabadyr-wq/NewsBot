@'
# NewsBot

Telegram-бот на Python: сам ищет свежие новости по ключевым словам через GNews API, отсеивает нерелевантные и дублирующиеся материалы, переводит их на второй язык и публикует в Telegram-канал.

## Возможности

- поиск новостей на русском и английском через GNews API (паузы и повтор при лимите частоты);
- фильтр по ключевым словам в заголовке;
- защита от дублей: по ссылке и по похожести заголовков (SQLite);
- двуязычные посты: оригинал и автоматический перевод (MyMemory, резерв Google);
- публикация в канал с HTML-оформлением, лимит сообщений за запуск;
- ночная пауза (по умолчанию 00:00-08:00 МСК);
- режимы --dry-run (без публикации) и --force (игнорировать ночную паузу);
- запуск по расписанию (Планировщик заданий Windows, раз в час).

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
    MYMEMORY_EMAIL=ваша почта (увеличивает суточный лимит перевода)

Бот должен быть администратором канала с правом публикации сообщений.

## Запуск

    python -m src.main --dry-run   # показать, что будет отправлено
    python -m src.main             # опубликовать
    python -m src.main --force     # опубликовать, игнорируя ночную паузу
    python -m pytest -q            # тесты

Ключевые слова, поисковые запросы, лимиты и часы ночной паузы настраиваются в src/config.py.

## Автозапуск (Windows)

Скрипт run.ps1 запускает бота и пишет лог в logs/newsbot.log. Его вызывает задание Планировщика, которое срабатывает раз в час.

## Структура

- src/news_client.py - запросы к GNews
- src/dedup.py - фильтр и защита от дублей
- src/translator.py - перевод (MyMemory, Google)
- src/formatter.py - оформление сообщений
- src/quiet.py - ночная пауза
- src/main.py - главный сценарий
- run.ps1 - запуск для Планировщика заданий

## Автор

Stanislav Sabadyr
