from typing import Dict, Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerMiddleware(BaseMiddleware):

    def __init__(self, scheduler: AsyncIOScheduler):
        self._scheduler = scheduler

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]):
        data["scheduler"] = self._scheduler
        return await handler(event, data)
