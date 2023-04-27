from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.sql.base import ExecutableOption

from bot.models import Question
from bot.repositories.base import BaseRepository


class QuestionFilter(BaseModel):
    event_id: Optional[int] = None


class QuestionRepository(BaseRepository[Question]):
    __model__ = Question

    async def find(
            self,
            question_filter: QuestionFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Sequence[Question]:
        query = select(self.__model__)

        if question_filter.event_id is not None:
            query = query.filter_by(event_id=question_filter.event_id)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            question_filter: QuestionFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[Question]:
        query = select(self.__model__).limit(1)

        if question_filter.event_id is not None:
            query = query.filter_by(event_id=question_filter.event_id)

        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()

    async def delete_many(self, question_filter: QuestionFilter) -> None:
        query = delete(self.__model__)

        if question_filter.event_id is not None:
            query = query.filter_by(event_id=question_filter.event_id)

        await self._session.execute(query)
