from aiogram.fsm.state import StatesGroup, State


class RegistrationForm(StatesGroup):
    form = State()
    confirm = State()
