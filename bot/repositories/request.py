from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bot.models import Answer, Request
from bot.repositories.base import BaseRepository


class RequestFilter(BaseModel):
    user_id: Optional[int] = None
    event_id: Optional[int] = None

    limit: Optional[int] = None
    offset: Optional[int] = None


class RequestRepository(BaseRepository[Request]):
    __model__ = Request

    async def get_by_id(self, answer_id: int) -> Optional[Request]:
        return (await self._session.scalars(
            select(self.__model__)
            .where(Answer.id == answer_id)
            .options(joinedload("*"))
            .limit(1)
        )).first()

    async def find(self, request_filter: RequestFilter) -> Sequence[Request]:
        query = select(self.__model__).options(joinedload("*"))

        if request_filter.user_id is not None:
            query = query.filter_by(user_id=request_filter.user_id)
        if request_filter.event_id is not None:
            query = query.filter_by(event_id=request_filter.event_id)

        if request_filter.limit is not None:
            query = query.limit(request_filter.limit)
        if request_filter.offset is not None:
            query = query.offset(request_filter.offset)

        return (await self._session.scalars(query)).all()
