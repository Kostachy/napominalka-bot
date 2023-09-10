from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.bot_config import config

DATABASE_URL = f"postgresql+asyncpg://{config.postgres.db_user}:{config.postgres.db_pass}@{config.postgres.db_host}:{config.postgres.db_port}/{config.postgres.db_name}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass