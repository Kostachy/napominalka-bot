from datetime import datetime, date
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, CommandStart, Text
from keyboards.keyboard_utils import inline_keyboard_1, default_keybord, inline_keyboard_2, inline_keyboard_3
from lexicon.lexicon_ru import START_DESCRIPTION, HELP_DESCRIPTION
from aiogram3_calendar import simple_cal_callback, SimpleCalendar
from filters.general_filters import IsTask

from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from database import task_database


router: Router = Router()


class FSMFillForm(StatesGroup):
    fill_date = State()
    fill_task = State()
    fill_time = State()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    # if message.from_user.id not in await task_database.get_all_users_id():
    #     await task_database.set_datas(message.from_user.id, message.from_user.username)
    await message.answer(START_DESCRIPTION, reply_markup=default_keybord)


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'Нажимите на кнопку')
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.reply(HELP_DESCRIPTION, reply_markup=default_keybord)


# Хэндлер для записи списка задач
@router.message(Text(text='Записать напоминалку', ignore_case=True), StateFilter(default_state))
async def get_list_of_tasks(message: Message, state: FSMContext):
    await message.answer('Выбери дату', reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(FSMFillForm.fill_date)


@router.callback_query(StateFilter(FSMFillForm.fill_date), simple_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, my_date = await SimpleCalendar().process_selection(callback_query, callback_data)
    await state.update_data(date=callback_query.data)
    if selected:
        print(type(my_date))
        print(selected)
        await callback_query.message.edit_text(f'Вы выбрали: {my_date.strftime("%d.%m.%Y")}',
                                               reply_markup=inline_keyboard_1)
        await callback_query.answer()
        await state.set_state(FSMFillForm.fill_task)

        # global set_for_date
        # set_for_date.add(date)
        # users[callback_query.from_user.id]['date'] = set_for_date
        # print(users)


@router.callback_query(StateFilter(FSMFillForm.fill_task), Text(text='task_button_pressed', ignore_case=True))
async def write_task_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text('Напишите мне все свои задачи')


@router.message(StateFilter(FSMFillForm.fill_task), F.text.isalpha())
async def set_tasks(message: Message, state: FSMContext):
    await state.update_data(task=message.text)
    await message.answer('Отлично! Теперь задай мне время в формате ЧАСЫ:МИНИНУТЫ')
    await state.set_state(FSMFillForm.fill_time)


@router.message(StateFilter(FSMFillForm.fill_time), F.text.isalpha())
async def set_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer('Напоминалка успешна задана!')
    await state.set_state(default_state)


# Узнать работает ли если пользователь в другой часовой зоне
@router.message(Text(text='Узнать дату на сегодня'))
async def get_today_date(message: Message):
    today_date = date.today().strftime('%d.%m.%Y')
    await message.answer(f'Cегодняшняя дата: {today_date}', reply_markup=default_keybord)


# Обработка любых сообщений
@router.message()
async def get_answer_to_any_message(message: Message):
    await message.answer('Вы ввели некоректные данные.\nВыберите доступные варианты из меню')
