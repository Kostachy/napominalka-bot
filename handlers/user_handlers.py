import logging
import re
from datetime import datetime, timedelta
from typing import Union

from aiogram import Bot, F, Router
from aiogram3_calendar import SimpleCalendar, simple_cal_callback
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from db.crud import DatetimeCRUD, UserCRUD
from sheduler import sched

# from middlewares.mid_for_scheduler import SchedulerMiddleware
from utils import FSMfill
from utils.keybords.user_keybord import default_keybord, origin_keybord
from utils.lexicon import HELP_DESCRIPTION, START_DESCRIPTION

user_router = Router()


async def send_some_message(bot: Bot, message: str, chat_id: Union[int, str]):
    await bot.send_message(text="⏰НАПОМИНАЛКА⏰", chat_id=chat_id)
    await bot.send_message(text=message, chat_id=chat_id)


@user_router.message(CommandStart())
async def get_started(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(START_DESCRIPTION, reply_markup=origin_keybord)
    if not await UserCRUD.read_user(message.from_user.id):
        await UserCRUD.add(
            user_id=message.from_user.id, username=message.from_user.username
        )


@user_router.message(Command("help"))
async def get_helped(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(HELP_DESCRIPTION, reply_markup=origin_keybord)


@user_router.message(Command(commands=["cancel"]))
@user_router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=origin_keybord)


@user_router.message(F.text == "Задать дату-время")
async def write_napominalka(message: Message, state: FSMContext):
    await message.reply(
        "Пожалуйста выберите дату: ",
        reply_markup=await SimpleCalendar().start_calendar(),
    )
    await state.set_state(FSMfill.choosing_date)


@user_router.message(FSMfill.choosing_date)
async def cancel_cal_date(message: Message):
    await message.answer("Пожалуйста выберите дату из появившегося меню")


@user_router.callback_query(FSMfill.choosing_date, simple_cal_callback.filter())
async def chose_date(
    callback_query: CallbackQuery, callback_data: dict, state: FSMContext
):
    selected, selected_date = await SimpleCalendar().process_selection(
        callback_query, callback_data
    )
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали {selected_date.strftime("%d/%m/%Y")}\nТеперь укажите время в формате HH:MM'
        )
        selected_date = str(selected_date).split("-")
        other = selected_date[-1].split()
        selected_date.pop(-1)
        selected_date.insert(2, other[0])
        selected_date = [int(i) for i in selected_date]
        await state.update_data(selected_date=selected_date)
        await state.set_state(FSMfill.choosing_time)


@user_router.message(
    FSMfill.choosing_time,
    lambda message: re.match(r"\d\d:\d\d", message.text)
)
async def chose_time(message: Message, state: FSMContext):
    selected_time = [int(i) for i in message.text.split(":")]
    await state.update_data(selected_time=selected_time)
    await message.answer("Теперь выберите действие", reply_markup=default_keybord)
    await state.set_state(FSMfill.choosing_func)


@user_router.message(FSMfill.choosing_time)
async def cancel_cal_time(message: Message):
    await message.answer("Пожалуйста запишите время в формате HH:MM")


@user_router.message(
    FSMfill.choosing_func,
    F.text.in_(
        ["Записать напоминалку", "Удалить напоминалку", "Редактировать напоминалку"]
    ),
)
async def choose_func(message: Message, state: FSMContext):
    if message.text == "Записать напоминалку":
        await message.answer("Запишите текст напоминалки")
        await state.set_state(FSMfill.choosing_task)

    elif message.text == "Удалить напоминалку":
        datetime_date = await state.get_data()
        time_for_sheduler = datetime(
            year=datetime_date["selected_date"][0],
            month=datetime_date["selected_date"][1],
            day=datetime_date["selected_date"][2],
        ) + timedelta(
            hours=datetime_date["selected_time"][0],
            minutes=datetime_date["selected_time"][1],
        )
        try:
            job_id = await DatetimeCRUD.get_job_id(
                sch_datetime=time_for_sheduler, user_id=message.from_user.id
            )
            sched.remove_job(job_id[0])
            await DatetimeCRUD.delete(
                sch_datetime=time_for_sheduler, user_id=message.from_user.id
            )
            await message.answer(
                "Напоминалка успешна удалена!", reply_markup=origin_keybord
            )
            await state.clear()
        except Exception as err:
            logging.error(err, exc_info=True)
            await message.answer(
                "Упс... Что-то пошло не так.\nВидимо на эту дату ничего не записано",
                reply_markup=origin_keybord,
            )
            await state.clear()


@user_router.message(FSMfill.choosing_func)
async def cancel_cal_func(message: Message):
    await message.answer("Пожалуйста выберите доступное действие из меню")


@user_router.message(FSMfill.choosing_task, F.text)
async def write_text_napomninalki(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(tasks=message.text)
    user_data = await state.get_data()

    time_for_sheduler = datetime(
        year=user_data["selected_date"][0],
        month=user_data["selected_date"][1],
        day=user_data["selected_date"][2],
    ) + timedelta(
        hours=user_data["selected_time"][0], minutes=user_data["selected_time"][1]
    )

    await DatetimeCRUD.add(
        sch_datetime=time_for_sheduler,
        user_id=message.from_user.id,
        reminder_text=user_data["tasks"],
        job_id=sched.add_job(
            func=send_some_message,
            trigger="date",
            run_date=time_for_sheduler,
            kwargs={
                "bot": bot,
                "message": user_data["tasks"],
                "chat_id": message.from_user.id,
            },
        ).id,
    )
    await message.answer(
        "Напоминалка успешно записана!\nЯ отправлю вам уведомление как только наступит время",
        reply_markup=origin_keybord,
    )
    await state.clear()


@user_router.message()
async def other_messages(message: Message):
    await message.answer("Выберите кнопку из меню", reply_markup=origin_keybord)
