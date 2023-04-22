from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.buttons import YES, NO

CONFIRM_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text=YES),
        KeyboardButton(text=NO)
    ]],
    resize_keyboard=True
)
