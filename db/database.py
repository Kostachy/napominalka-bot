from typing import Any

from sqlalchemy import (
    Insert,
    Select,
    Update,
    Result,
    Delete,
    NullPool
)

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config.bot_config import config

if config.tg_bot.mode == "TEST":
    DATABASE_URL = f"postgresql+asyncpg://{config.postgres.db_user}:{config.postgres.db_pass}@{config.postgres.db_host}:{config.postgres.db_port}/{config.postgres.db_name_test}"
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = f"postgresql+asyncpg://{config.postgres.db_user}:{config.postgres.db_pass}@{config.postgres.db_host}:{config.postgres.db_port}/{config.postgres.db_name}"
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def fetch_one(select_query: Select | Insert | Update) -> Any | None:
    async with async_session_maker() as session:
        result: Result = await session.execute(select_query)
        return result.one_or_none()


async def fetch_all(select_query: Select | Insert | Update) -> Result | list | Any:
    async with async_session_maker() as session:
        result: Result = await session.execute(select_query)
        return result.all()


async def new_execute(select_query: Insert | Update | Delete) -> None:
    async with async_session_maker() as session:
        await session.execute(select_query)
        await session.commit()
