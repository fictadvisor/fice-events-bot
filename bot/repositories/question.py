from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bot.models import Question
from bot.repositories.base import BaseRepository


class QuestionFilter(BaseModel):
    event_id: Optional[int] = None


class QuestionRepository(BaseRepository[Question]):
    __model__ = Question

    async def get_by_id(self, question_id: int) -> Optional[Question]:
        return (await self._session.scalars(
            select(self.__model__)
            .where(Question.id == question_id)
            .options(joinedload("*"))
            .limit(1)
        )).first()

    async def find(self, question_filter: QuestionFilter, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[Question]:
        query = select(self.__model__).options(joinedload("*"))

        if question_filter.event_id is not None:
            query = query.filter_by(event_id=question_filter.event_id)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return (await self._session.scalars(query)).all()

    async def find_one(self, question_filter: QuestionFilter, offset: Optional[int] = None) -> Optional[Question]:
        query = select(self.__model__).options(joinedload("*")).limit(1)

        if question_filter.event_id is not None:
            query = query.filter_by(event_id=question_filter.event_id)

        if offset is not None:
            query = query.offset(offset)

        return (await self._session.scalars(query)).first()
