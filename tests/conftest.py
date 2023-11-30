import asyncio
from typing import Generator
from db.database import Base, engine
from config.bot_config import config
import pytest


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    assert config.tg_bot.mode == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
