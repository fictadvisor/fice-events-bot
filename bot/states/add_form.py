from aiogram.fsm.state import StatesGroup, State


class AddQuestionForm(StatesGroup):
    question = State()


class AddEventForm(StatesGroup):
    title = State()
    description = State()
    date = State()

    confirm = State()
