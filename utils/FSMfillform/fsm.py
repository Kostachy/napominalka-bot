from aiogram.fsm.state import State, StatesGroup


class FSMfill(StatesGroup):
    choosing_date = State()
    choosing_time = State()
    choosing_task = State()
    waiting_job = State()
