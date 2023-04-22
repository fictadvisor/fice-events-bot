from aiogram.fsm.state import StatesGroup, State


class StartForm(StatesGroup):
    fullname = State()
    faculty = State()
    group = State()

    confirm = State()
