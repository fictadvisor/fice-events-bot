from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select, func, delete
from sqlalchemy.sql.base import ExecutableOption

from bot.models import Event
from bot.repositories.base import BaseRepository


class EventFilter(BaseModel):
    title: Optional[str] = None
    published: Optional[bool] = None
    date: Optional[datetime] = None

    ended: Optional[bool] = None


class EventRepository(BaseRepository[Event]):
    __model__ = Event

    async def find(
            self,
            event_filter: EventFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Sequence[Event]:
        query = select(self.__model__)

        if event_filter.title is not None:
            query = query.filter_by(title=event_filter.title)
        if event_filter.published is not None:
            query = query.filter_by(published=event_filter.published)
        if event_filter.date is not None:
            query = query.filter_by(date=event_filter.date)
        if event_filter.ended is not None:
            if event_filter.ended:
                query = query.where(Event.date < func.now())
            else:
                query = query.where(Event.date > func.now())

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            event_filter: EventFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[Event]:
        query = select(self.__model__).limit(1)

        if event_filter.title is not None:
            query = query.filter_by(title=event_filter.title)
        if event_filter.date is not None:
            query = query.filter_by(date=event_filter.date)
        if event_filter.ended is not None:
            if event_filter.ended:
                query = query.where(Event.date < func.now())
            else:
                query = query.where(Event.date > func.now())

        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()

    async def delete_many(self, event_filter: EventFilter) -> None:
        query = delete(self.__model__)

        if event_filter.title is not None:
            query = query.filter_by(title=event_filter.title)
        if event_filter.date is not None:
            query = query.filter_by(date=event_filter.date)
        if event_filter.ended is not None:
            if event_filter.ended:
                query = query.where(Event.date < func.now())
            else:
                query = query.where(Event.date > func.now())

        await self._session.execute(query)
