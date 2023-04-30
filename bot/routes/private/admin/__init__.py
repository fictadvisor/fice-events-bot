from aiogram import Router

from bot.routes.private.admin.events import events_router
from bot.routes.private.admin.menu import menu_router

admin_router = Router()

admin_router.include_router(menu_router)
admin_router.include_router(events_router)
