from aiogram.fsm.state import StatesGroup, State


class FeedbackForm(StatesGroup):
    form = State()
