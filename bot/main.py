import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.middlewares.sessionmaker import SessionMaker
from bot.routes.private.start import start_router
from bot.settings import settings

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


async def main() -> None:
    engine = create_async_engine(
        URL.create(
            "postgresql+asyncpg",
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD.get_secret_value(),
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
        )
    )
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    storage = RedisStorage(Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        username=settings.REDIS_USERNAME,
        password=settings.REDIS_PASSWORD.get_secret_value()
    ))

    bot = Bot(token=settings.TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)

    dp.update.middleware(SessionMaker(sessionmaker))

    for router in [start_router]:
        dp. include_router(router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
