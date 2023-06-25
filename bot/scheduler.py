from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload

from bot.messages.events import REMINDER
from bot.models import Event, Request
from bot.repositories.event import EventRepository, EventFilter


class Scheduler:
    def __init__(self, bot: Bot, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._bot = bot
        self._session_maker = session_maker
        self._scheduler = AsyncIOScheduler(timezone="Europe/Kiev")

        self.setup_jobs()

    def setup_jobs(self):
        self._scheduler.add_job(self.tomorrow, 'cron', hour="17", minute="30")

    async def start(self) -> None:
        self._scheduler.start()

    async def tomorrow(self) -> None:
        async with self._session_maker() as session:
            event_repository = EventRepository(session)
            tomorrow = await event_repository.find(
                EventFilter(
                    days_interval=1
                ),
                options=[
                    selectinload(Event.requests).subqueryload(Request.user)
                ]
            )
            for event in tomorrow:
                for request in event.requests:
                    try:
                        await self._bot.send_message(request.user_id, await REMINDER.render_async(event=event))
                    except:
                        pass
