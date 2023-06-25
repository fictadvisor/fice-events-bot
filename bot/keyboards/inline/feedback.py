from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.inline.buttons import FEEDBACK_EVENT


class FeedbackEvent(CallbackData, prefix="feedback"):
    event_id: int


async def get_feedback_keyboard(event_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=FEEDBACK_EVENT, callback_data=FeedbackEvent(event_id=event_id).pack())
    ]])
