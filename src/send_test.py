import asyncio

from telegram import Bot
from telegram.error import TelegramError

from src import config


async def main() -> None:
    token = config.require("TELEGRAM_BOT_TOKEN", config.TELEGRAM_BOT_TOKEN)
    channel = config.require("TELEGRAM_CHANNEL_ID", config.TELEGRAM_CHANNEL_ID)

    async with Bot(token) as bot:
        me = await bot.get_me()
        print(f"Бот авторизован: @{me.username}")
        try:
            msg = await bot.send_message(
                chat_id=channel,
                text="✅ NewsBot подключен к каналу. Тестовое сообщение.",
            )
            print(f"Сообщение отправлено, id={msg.message_id}")
        except TelegramError as e:
            print(f"Ошибка Telegram: {e}")


if __name__ == "__main__":
    asyncio.run(main())
