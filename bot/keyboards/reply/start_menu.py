from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.keyboards.reply.buttons import ADMIN_PANEL
from bot.keyboards.reply.buttons import EVENTS


async def get_start_menu(is_moderator: bool) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text=EVENTS)
    if is_moderator:
        builder.button(text=ADMIN_PANEL)
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
