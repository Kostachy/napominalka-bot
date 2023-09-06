from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram3_calendar import simple_cal_callback, SimpleCalendar

from db.models.model import Users
from utils.keybords.user_keybord import default_keybord
from utils.lexicon import START_DESCRIPTION, HELP_DESCRIPTION

from db.crud import UserCRUD

user_router = Router()


@user_router.message(CommandStart())
async def get_started(message: Message):
    await message.answer(START_DESCRIPTION, reply_markup=default_keybord)
    print(await UserCRUD.read_user(message.from_user.id))
    if not await UserCRUD.read_user(message.from_user.id):
        await UserCRUD.create_user(user_id=message.from_user.id, username=message.from_user.username)


@user_router.message(Command('help'))
async def get_started(message: Message):
    await message.answer(HELP_DESCRIPTION, reply_markup=default_keybord)


@user_router.message(F.text == 'Записать напоминалку')
async def nav_cal_handler(message: Message):
    await message.reply("Пожалуйста выберите дату: ", reply_markup=await SimpleCalendar().start_calendar())


# simple calendar usage
@user_router.callback_query(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали {date.strftime("%d/%m/%Y")}\nТеперь укажите время в формате HH:MM')


@user_router.message()
async def message_with_text(message: Message):
    await message.answer("Выберите кнопку из меню")
