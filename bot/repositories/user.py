from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.sql.base import ExecutableOption

from bot.constants.roles import Roles
from bot.models import User
from bot.repositories.base import BaseRepository


class UserFilter(BaseModel):
    fullname: Optional[str] = None
    username: Optional[str] = None
    faculty: Optional[str] = None
    group: Optional[str] = None
    role: Optional[Roles] = None


class UserRepository(BaseRepository[User]):
    __model__ = User

    async def find(
            self,
            user_filter: UserFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Sequence[User]:
        query = select(self.__model__)

        if user_filter.fullname is not None:
            query = query.filter_by(fullname=user_filter.fullname)
        if user_filter.username is not None:
            query = query.filter_by(username=user_filter.username)
        if user_filter.faculty is not None:
            query = query.filter_by(faculty=user_filter.faculty)
        if user_filter.group is not None:
            query = query.filter_by(group=user_filter.group)
        if user_filter.role is not None:
            query = query.filter_by(role=user_filter.role)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            user_filter: UserFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[User]:
        query = select(self.__model__).limit(1)

        if user_filter.fullname is not None:
            query = query.filter_by(fullname=user_filter.fullname)
        if user_filter.username is not None:
            query = query.filter_by(username=user_filter.username)
        if user_filter.faculty is not None:
            query = query.filter_by(faculty=user_filter.faculty)
        if user_filter.group is not None:
            query = query.filter_by(group=user_filter.group)
        if user_filter.role is not None:
            query = query.filter_by(role=user_filter.role)

        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()

    async def delete_many(self, user_filter: UserFilter) -> None:
        query = delete(self.__model__)

        if user_filter.fullname is not None:
            query = query.filter_by(fullname=user_filter.fullname)
        if user_filter.username is not None:
            query = query.filter_by(username=user_filter.username)
        if user_filter.faculty is not None:
            query = query.filter_by(faculty=user_filter.faculty)
        if user_filter.group is not None:
            query = query.filter_by(group=user_filter.group)
        if user_filter.role is not None:
            query = query.filter_by(role=user_filter.role)

        await self._session.execute(query)
