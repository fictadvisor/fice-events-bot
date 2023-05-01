from aiogram.fsm.state import StatesGroup, State


class EditForm(StatesGroup):
    title = State()
    description = State()
    date = State()
    question = State()
