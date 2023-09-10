from aiogram.fsm.state import StatesGroup, State


class FSMfill(StatesGroup):
    choosing_date = State()
    choosing_time = State()
    choosing_task = State()
    waiting_job = State()


class FSMfillToDelete(StatesGroup):
    choosing_date = State()
    choosing_time = State()
    choosing_task = State()
