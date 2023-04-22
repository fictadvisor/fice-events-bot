from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.keyboards.buttons import SEE_EVENTS, ADMIN_PANEL


async def get_main_menu(is_admin: bool = False) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=SEE_EVENTS)
    if is_admin:
        builder.button(text=ADMIN_PANEL)

    return builder.as_markup(
        resize_keyboard=True
    )
