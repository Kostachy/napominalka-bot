from aiogram.fsm.state import State, StatesGroup


class FSMfill(StatesGroup):
    choosing_date = State()
    choosing_time = State()
    choosing_func = State()
    choosing_task = State()
    fill_delete = State()
