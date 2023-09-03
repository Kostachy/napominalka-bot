from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from utils.keybords.user_keybord import default_keybord
from utils.lexicon import START_DESCRIPTION

user_router = Router()


@user_router.message(CommandStart())
async def get_started(message: Message):
    await message.answer(START_DESCRIPTION, reply_markup=default_keybord)
    # тут будет проверка зареган ли юзер в боте или нет


@user_router.message(F.text)
async def message_with_text(message: Message):
    await message.answer("Это текстовое сообщение!")


@user_router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer("Это стикер!")


@user_router.message(F.animation)
async def message_with_gif(message: Message):
    await message.answer("Это GIF!")
