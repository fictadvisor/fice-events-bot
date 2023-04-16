import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.settings import settings

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
