from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.inline.buttons import REGISTER_USER

REGISTER_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text=REGISTER_USER, callback_data="register")
]])
