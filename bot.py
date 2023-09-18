import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config.bot_config import config
from handlers.user_handlers import user_router
from sheduler import sched

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{config.webhook_config.BASE_WEBHOOK_URL}{config.webhook_config.WEBHOOK_PATH}",
        secret_token=config.webhook_config.WEBHOOK_SECRET,
    )


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    redis: Redis = Redis(
        host=config.redis_db.redis_host,
        port=config.redis_db.redis_port,
        password=config.redis_db.redis_pass,
    )

    session = AiohttpSession()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML", session=session)
    # app = web.Application()

    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_router(user_router)
    sched.start()

    if config.webhook_config.USE_WEBHOOK:
        dp.startup.register(on_startup)
        app = web.Application()
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=config.webhook_config.WEBHOOK_SECRET,
        )
        webhook_requests_handler.register(app, path=config.webhook_config.WEBHOOK_PATH)

        # Mount dispatcher startup and shutdown hooks to aiohttp application
        setup_application(app, dp, bot=bot)

    else:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
