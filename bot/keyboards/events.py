from typing import Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.models import Event


class SelectEvent(CallbackData, prefix="events"):
    event_id: int


class RegisterEvent(CallbackData, prefix="event"):
    event_id: int


async def get_events_keyboard(events: Sequence[Event]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for event in events:
        builder.button(text=event.title, callback_data=SelectEvent(event_id=event.id))

    return builder.as_markup()


async def get_register_keyboard(event_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Зареєструватись", callback_data=RegisterEvent(event_id=event_id).pack())
    ]])
