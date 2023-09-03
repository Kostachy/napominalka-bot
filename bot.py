import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import settings
from handlers.user_handlers import user_router


async def main():
    logging.basicConfig(level=logging.INFO)

    bot: Bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
