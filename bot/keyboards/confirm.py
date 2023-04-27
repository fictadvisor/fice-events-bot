from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.buttons import YES, NO


class Select(str, Enum):
    YES = "yes"
    NO = "no"


class ConfirmData(CallbackData, prefix="confirm"):
    select: Select


CONFIRM_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text=YES, callback_data=ConfirmData(select=Select.YES).pack()),
        InlineKeyboardButton(text=NO, callback_data=ConfirmData(select=Select.NO).pack())
    ]],
)
