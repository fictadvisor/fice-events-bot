from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bot.models import Answer
from bot.repositories.base import BaseRepository


class AnswerFilter(BaseModel):
    request_id: Optional[int] = None
    question_id: Optional[int] = None


class AnswerRepository(BaseRepository[Answer]):
    __model__ = Answer

    async def get_by_id(self, answer_id: int) -> Optional[Answer]:
        return (await self._session.scalars(
            select(self.__model__)
            .where(Answer.id == answer_id)
            .options(joinedload("*"))
            .limit(1)
        )).first()

    async def find(self, answer_filter: AnswerFilter, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[Answer]:
        query = select(self.__model__).options(joinedload("*"))

        if answer_filter.request_id is not None:
            query = query.filter_by(request_id=answer_filter.request_id)
        if answer_filter.question_id is not None:
            query = query.filter_by(question_id=answer_filter.question_id)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return (await self._session.scalars(query)).all()

    async def find_one(self, answer_filter: AnswerFilter, offset: Optional[int] = None) -> Optional[Answer]:
        query = select(self.__model__).options(joinedload("*")).limit(1)

        if answer_filter.request_id is not None:
            query = query.filter_by(request_id=answer_filter.request_id)
        if answer_filter.question_id is not None:
            query = query.filter_by(question_id=answer_filter.question_id)

        if offset is not None:
            query = query.offset(offset)

        return (await self._session.scalars(query)).first()
