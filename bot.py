import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import settings


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
