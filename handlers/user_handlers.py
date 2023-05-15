from datetime import date, time, datetime
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, CommandStart, Text
from keyboards.keyboard_utils import inline_keyboard, default_keybord
from lexicon.lexicon_ru import START_DESCRIPTION, HELP_DESCRIPTION
from aiogram3_calendar import simple_cal_callback, SimpleCalendar
from filters.general_filters import IsTask


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
@router.message(Text(text='Записать список задач на день', ignore_case=True))
async def get_list_of_tasks(message: Message):
    await message.answer('Напиши мне нужные вам задачи', reply_markup=default_keybord)


@router.message(Text(startswith='Задачи', ignore_case=True))
async def set_tasks(message: Message):
    global tasks
    tasks.append(message.text)
    await message.answer('Теперь выберите дату когда вам стоит о них напомнить')


# Узнать работает ли если пользователь в другой часовой зоне
@router.message(Text(text='Узнать дату на сегодня'))
async def get_today_date(message: Message):
    today_date = date.today().strftime('%d.%m.%Y')
    await message.answer(f'Cегодняшняя дата: {today_date}', reply_markup=default_keybord)


@router.message(Text(text='Задать дату', ignore_case=True))
async def set_date(message: Message):
    await message.answer('Пожалуйста выберите дату:', reply_markup=await SimpleCalendar().start_calendar())


# колбэк календаря
@router.callback_query(simple_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали: {date.strftime("%d.%m.%Y")}',
            reply_markup=default_keybord)
        global set_for_date
        set_for_date.add(date)
        users[callback_query.from_user.id]['date'] = set_for_date
        print(users)


# Обработка любых сообщений
@router.message()
async def get_answer_to_any_message(message: Message):
    await message.answer('Вы ввели некоректные данные.\nВыберите доступные варианты из меню')
