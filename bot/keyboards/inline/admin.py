from enum import Enum
from typing import Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.constants.request_types import RequestTypes
from bot.keyboards.inline.buttons import ADD_EVENT, BACK, DELETE, ADD_QUESTION, ALL_QUESTIONS, EDIT_EVENT_TITLE, \
    EDIT_EVENT_DESCRIPTION, EDIT_QUESTION_TEXT, ALL_EVENTS, EXPORT, EDIT_EVENT_DATE, PUBLISH, HIDE, EDIT_EVENT, SEND, \
    FEEDBACK, EXPORT_FEEDBACK
from bot.models import Event, Question


async def get_admin_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=ALL_EVENTS, callback_data="admin:events")

    return builder.as_markup()


class EventInfo(CallbackData, prefix="event_info"):
    event_id: int


async def get_events_keyboard(events: Sequence[Event]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for event in events:
        builder.button(text=event.title, callback_data=EventInfo(event_id=event.id))

    builder.button(text=ADD_EVENT, callback_data="add_event")

    builder.adjust(1)
    return builder.as_markup()


class EventActions(str, Enum):
    EDIT = "edit"
    TITLE = "title"
    DESCRIPTION = "description"
    QUESTIONS = "questions"
    FEEDBACK = "feedback"
    DATE = "date"

    SEND = "send"

    PUBLISH = "publish"
    EXPORT = "export"
    EXPORT_FEEDBACK = "export_feedback"
    DELETE = "delete"


class EventAction(CallbackData, prefix="event_action"):
    event_id: int
    action: EventActions


async def get_event_keyboard(event_id: int, is_published: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=EDIT_EVENT, callback_data=EventAction(event_id=event_id, action=EventActions.EDIT))
    builder.button(text=ALL_QUESTIONS, callback_data=EventAction(event_id=event_id, action=EventActions.QUESTIONS))
    builder.button(text=FEEDBACK, callback_data=EventAction(event_id=event_id, action=EventActions.FEEDBACK))

    text = HIDE if is_published else PUBLISH
    builder.button(text=text, callback_data=EventAction(event_id=event_id, action=EventActions.PUBLISH))
    builder.button(text=EXPORT, callback_data=EventAction(event_id=event_id, action=EventActions.EXPORT))
    builder.button(text=EXPORT_FEEDBACK, callback_data=EventAction(event_id=event_id, action=EventActions.EXPORT_FEEDBACK))
    builder.button(text=SEND, callback_data=EventAction(event_id=event_id, action=EventActions.SEND))
    builder.button(text=DELETE, callback_data=EventAction(event_id=event_id, action=EventActions.DELETE))
    builder.button(text=BACK, callback_data="admin:events")
    builder.adjust(1)

    return builder.as_markup()


async def get_edit_keyboard(event_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=EDIT_EVENT_TITLE, callback_data=EventAction(event_id=event_id, action=EventActions.TITLE))
    builder.button(text=EDIT_EVENT_DESCRIPTION,
                   callback_data=EventAction(event_id=event_id, action=EventActions.DESCRIPTION))
    builder.button(text=EDIT_EVENT_DATE, callback_data=EventAction(event_id=event_id, action=EventActions.DATE))
    builder.button(text=BACK, callback_data=EventInfo(event_id=event_id))
    builder.adjust(1)

    return builder.as_markup()


class QuestionInfo(CallbackData, prefix="questions"):
    question_id: int
    type: RequestTypes


class AddQuestion(CallbackData, prefix="add_question"):
    event_id: int
    type: RequestTypes


async def get_questions_keyboard(event_id: int, questions: Sequence[Question],
                                 request_type: RequestTypes = RequestTypes.REGISTER) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for question in questions:
        builder.button(text=question.text, callback_data=QuestionInfo(question_id=question.id, type=request_type))

    builder.button(text=ADD_QUESTION, callback_data=AddQuestion(event_id=event_id, type=request_type))
    builder.button(text=BACK, callback_data=EventInfo(event_id=event_id))
    builder.adjust(1)

    return builder.as_markup()


class EditTypes(str, Enum):
    EDIT = "edit"
    DELETE = "delete"


class EditQuestion(CallbackData, prefix="question"):
    type: EditTypes
    question_id: int


async def get_question_keyboard(event_id: int, question_id: int,
                                request_type: RequestTypes = RequestTypes.REGISTER) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=EDIT_QUESTION_TEXT, callback_data=EditQuestion(question_id=question_id, type=EditTypes.EDIT))
    builder.button(text=DELETE, callback_data=EditQuestion(question_id=question_id, type=EditTypes.DELETE))
    builder.button(text=BACK, callback_data=EventAction(event_id=event_id,
                                                        action=EventActions.QUESTIONS
                                                        if request_type == RequestTypes.REGISTER
                                                        else EventActions.FEEDBACK))
    builder.adjust(1)

    return builder.as_markup()
