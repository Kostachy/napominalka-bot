from datetime import datetime, date
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, CommandStart, Text
from keyboards.keyboard_utils import inline_keyboard_1, default_keybord, inline_keyboard_2, inline_keyboard_3
from lexicon.lexicon_ru import START_DESCRIPTION, HELP_DESCRIPTION
from aiogram3_calendar import simple_cal_callback, SimpleCalendar
from filters.general_filters import IsTask
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


router: Router = Router()
users: dict = {}
set_for_date = set()
tasks = []


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(START_DESCRIPTION, reply_markup=default_keybord)
    if message.from_user.id not in users:
        users[message.from_user.id] = {'date': None}
    print(users)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.reply(HELP_DESCRIPTION, reply_markup=default_keybord)


# Хэндлер для записи списка задач
@router.message(Text(text='Записать напоминалку', ignore_case=True))
async def get_list_of_tasks(message: Message):
    await message.answer('Выбери дату', reply_markup=await SimpleCalendar().start_calendar())


@router.callback_query(simple_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, my_date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        print(type(my_date))
        print(selected)
        await callback_query.message.edit_text(f'Вы выбрали: {my_date.strftime("%d.%m.%Y")}',
                                               reply_markup=inline_keyboard_1)
        await callback_query.answer()
        # global set_for_date
        # set_for_date.add(date)
        # users[callback_query.from_user.id]['date'] = set_for_date
        # print(users)


@router.callback_query(Text(startswith='task_button_pressed', ignore_case=True))
async def write_tasks(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Напишите мне все свои задачи', reply_markup=inline_keyboard_2)


@router.callback_query(Text(text='finish_task_button_pressed', ignore_case=True))
async def set_time(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Отлично! Теперь задай мне время', reply_markup=inline_keyboard_3)

# Узнать работает ли если пользователь в другой часовой зоне
@router.message(Text(text='Узнать дату на сегодня'))
async def get_today_date(message: Message):
    today_date = date.today().strftime('%d.%m.%Y')
    await message.answer(f'Cегодняшняя дата: {today_date}', reply_markup=default_keybord)


@router.message(Text(text='Задать дату', ignore_case=True))
async def set_date(message: Message):
    await message.answer('Пожалуйста выберите дату:', reply_markup=await SimpleCalendar().start_calendar())


# Обработка любых сообщений
@router.message()
async def get_answer_to_any_message(message: Message):
    await message.answer('Вы ввели некоректные данные.\nВыберите доступные варианты из меню')
