from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.sql.base import ExecutableOption

from bot.constants.request_types import RequestTypes
from bot.models import Request
from bot.repositories.base import BaseRepository


class RequestFilter(BaseModel):
    type: Optional[RequestTypes] = RequestTypes.REGISTER
    confirmed: Optional[bool] = None

    user_id: Optional[int] = None
    event_id: Optional[int] = None


class RequestRepository(BaseRepository[Request]):
    __model__ = Request

    async def find(
            self,
            request_filter: RequestFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Sequence[Request]:
        query = select(self.__model__)

        if request_filter.type is not None:
            query = query.filter_by(type=request_filter.type)
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
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            request_filter: RequestFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[Request]:
        query = select(self.__model__).limit(1)

        if request_filter.type is not None:
            query = query.filter_by(type=request_filter.type)
        if request_filter.confirmed is not None:
            query = query.filter_by(confirmed=request_filter.confirmed)

        if request_filter.user_id is not None:
            query = query.filter_by(user_id=request_filter.user_id)
        if request_filter.event_id is not None:
            query = query.filter_by(event_id=request_filter.event_id)

        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()

    async def delete_many(self, request_filter: RequestFilter) -> None:
        query = delete(self.__model__)

        if request_filter.type is not None:
            query = query.filter_by(type=request_filter.type)
        if request_filter.confirmed is not None:
            query = query.filter_by(confirmed=request_filter.confirmed)

        if request_filter.user_id is not None:
            query = query.filter_by(user_id=request_filter.user_id)
        if request_filter.event_id is not None:
            query = query.filter_by(event_id=request_filter.event_id)

        await self._session.execute(query)
