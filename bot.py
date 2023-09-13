import asyncio
import logging
# import ssl

# from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
# from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from sheduler import sched

from config.bot_config import config
from handlers.user_handlers import user_router

logger = logging.getLogger(__name__)


# async def on_startup(bot: Bot) -> None:
#     await bot.set_webhook(f"{config.webhook_config.BASE_WEBHOOK_URL}{config.webhook_config.WEBHOOK_PATH}",
#                           secret_token=config.webhook_config.WEBHOOK_SECRET)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    redis: Redis = Redis(host=config.redis_db.redis_host,
                         port=config.redis_db.redis_port,
                         password=config.redis_db.redis_pass)

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    # app = web.Application()

    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_router(user_router)
    sched.start()
    await dp.start_polling(bot)
    # webhook_requests_handler = SimpleRequestHandler(
    #     dispatcher=dp,
    #     bot=bot,
    #     secret_token=config.webhook_config.WEBHOOK_SECRET,
    # )
    # # Register webhook handler on application
    # webhook_requests_handler.register(app, path=config.webhook_config.WEBHOOK_PATH)
    #
    # # Mount dispatcher startup and shutdown hooks to aiohttp application
    # setup_application(app, dp, bot=bot)
    #
    # # # Generate SSL context
    # # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # # context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
    #
    # # And finally start webserver
    # web.run_app(app, host=config.webhook_config.WEB_SERVER_HOST,
    #             port=config.webhook_config.WEB_SERVER_PORT)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
