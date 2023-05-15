from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsTask(BaseFilter):
    def __init__(self, msg: Message):
        self.msg = msg.text.lower()

    async def __call__(self) -> bool:
        return 'задачи' in self.msg
