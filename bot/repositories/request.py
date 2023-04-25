from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bot.models import Request
from bot.repositories.base import BaseRepository


class RequestFilter(BaseModel):
    confirmed: Optional[bool] = None

    user_id: Optional[int] = None
    event_id: Optional[int] = None


class RequestRepository(BaseRepository[Request]):
    __model__ = Request

    async def get_by_id(self, request_id: int) -> Optional[Request]:
        return (await self._session.scalars(
            select(self.__model__)
            .where(Request.id == request_id)
            .options(joinedload("*"))
            .limit(1)
        )).first()

    async def find(self, request_filter: RequestFilter, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[Request]:
        query = select(self.__model__).options(joinedload("*"))

        if request_filter.confirmed is not None:
            query = query.filter_by(confirmed=request_filter.confirmed)

        if request_filter.user_id is not None:
            query = query.filter_by(user_id=request_filter.user_id)
        if request_filter.event_id is not None:
            query = query.filter_by(event_id=request_filter.event_id)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return (await self._session.scalars(query)).all()

    async def find_one(self, request_filter: RequestFilter, offset: Optional[int] = None) -> Optional[Request]:
        query = select(self.__model__).options(joinedload("*")).limit(1)

        if request_filter.confirmed is not None:
            query = query.filter_by(confirmed=request_filter.confirmed)

        if request_filter.user_id is not None:
            query = query.filter_by(user_id=request_filter.user_id)
        if request_filter.event_id is not None:
            query = query.filter_by(event_id=request_filter.event_id)

        if offset is not None:
            query = query.offset(offset)

        return (await self._session.scalars(query)).first()
