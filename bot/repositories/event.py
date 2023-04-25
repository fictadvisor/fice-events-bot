from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bot.models import Event
from bot.repositories.base import BaseRepository


class EventFilter(BaseModel):
    title: Optional[str] = None
    date: Optional[datetime] = None


class EventRepository(BaseRepository[Event]):
    __model__ = Event

    async def get_by_id(self, event_id: int) -> Optional[Event]:
        return (await self._session.scalars(
            select(self.__model__)
            .where(Event.id == event_id)
            .options(joinedload("*"))
            .limit(1)
        )).first()

    async def find(self, event_filter: EventFilter, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[Event]:
        query = select(self.__model__).options(joinedload("*"))

        if event_filter.title is not None:
            query = query.filter_by(title=event_filter.title)
        if event_filter.date is not None:
            query = query.filter_by(date=event_filter.date)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return (await self._session.scalars(query)).all()

    async def find_one(self, event_filter: EventFilter, offset: Optional[int] = None) -> Optional[Event]:
        query = select(self.__model__).options(joinedload("*")).limit(1)

        if event_filter.title is not None:
            query = query.filter_by(title=event_filter.title)
        if event_filter.date is not None:
            query = query.filter_by(date=event_filter.date)

        if offset is not None:
            query = query.offset(offset)

        return (await self._session.scalars(query)).first()
