import re
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram3_calendar import simple_cal_callback, SimpleCalendar

from utils.keybords.user_keybord import default_keybord
from utils.lexicon import START_DESCRIPTION, HELP_DESCRIPTION

from db.crud import UserCRUD

user_router = Router()


class FSMfill(StatesGroup):
    choosing_date = State()
    choosing_time = State()
    choosing_task = State()


@user_router.message(CommandStart())
async def get_started(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(START_DESCRIPTION, reply_markup=default_keybord)
    print(await UserCRUD.read_user(message.from_user.id))
    if not await UserCRUD.read_user(message.from_user.id):
        await UserCRUD.create_user(user_id=message.from_user.id, username=message.from_user.username)


@user_router.message(Command('help'))
async def get_helped(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(HELP_DESCRIPTION, reply_markup=default_keybord)


@user_router.message(Command(commands=["cancel"]))
@user_router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=default_keybord
    )


@user_router.message(F.text == 'Записать напоминалку')
async def write_napominalka(message: Message, state: FSMContext):
    await message.reply("Пожалуйста выберите дату: ", reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(FSMfill.choosing_date)


@user_router.message(FSMfill.choosing_date)
async def cancel_cal_date(message: Message):
    await message.answer('Пожалуйста выберите дату из появившегося меню',
                         reply_markup=await SimpleCalendar().start_calendar())


@user_router.callback_query(FSMfill.choosing_date, simple_cal_callback.filter())
async def chose_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, selected_date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали {selected_date.strftime("%d/%m/%Y")}\nТеперь укажите время в формате HH:MM')
        await state.update_data(selected_date=selected_date)
        await state.set_state(FSMfill.choosing_time)


@user_router.message(FSMfill.choosing_time, lambda message: re.match(r'\d\d:\d\d', message.text))
async def chose_time(message: Message, state: FSMContext):
    selected_time = [int(i) for i in message.text.split(':')]
    await state.update_data(selected_time=selected_time)
    if selected_time[0] > 23 or selected_time[1] > 59:
        await message.answer('Вы указали неверное время\nПожалуйста запишите его в формате HH:MM')
    else:
        await message.answer('Теперь сделайте свою заметку')
    await state.set_state(FSMfill.choosing_task)


@user_router.message(FSMfill.choosing_time)
async def cancel_cal_time(message: Message):
    await message.answer('idi naxui')


@user_router.message(F.text)
async def write_text_napomninalki(message: Message, state: FSMContext):
    await state.update_data(tasks=message.text)
    user_data = await state.get_data()
    await message.answer(f'{user_data["selected_date"]}---{user_data["selected_time"]}----{user_data["tasks"]}')
    await message.answer(
        'Поздравляю!\nНапоминалка успешно записана\nЯ отправлю вам уведомление как только наступит время')
    await state.clear()


@user_router.message(FSMfill.choosing_task)
async def cancel_cal_time(message: Message):
    await message.answer('idi naxui 2')


@user_router.message()
async def other_messages(message: Message):
    await message.answer("Выберите кнопку из меню")
