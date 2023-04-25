from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

REGISTER_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Зареєструватись", callback_data="register")
]])
