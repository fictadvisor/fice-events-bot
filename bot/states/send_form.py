from aiogram.fsm.state import StatesGroup, State


class SendForm(StatesGroup):
    form = State()
    confirm = State()
