import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from sheduler import sched

from config.bot_config import config
from handlers.user_handlers import user_router


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    redis: Redis = Redis(host=config.redis_db.redis_host,
                         port=config.redis_db.redis_port,
                         password=config.redis_db.redis_pass)

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_router(user_router)

    sched.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
