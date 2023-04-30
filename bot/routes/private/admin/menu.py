from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.filters.is_moderaror import IsModerator
from bot.keyboards.admin import get_admin_menu
from bot.messages.admin import ADMIN_MENU

menu_router = Router()
menu_router.message.filter(IsModerator())
menu_router.callback_query.filter(IsModerator())


@menu_router.message(Command("admin"))
async def menu(message: Message) -> None:
    await message.answer(ADMIN_MENU, reply_markup=await get_admin_menu())
