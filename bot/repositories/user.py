from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bot.constants.roles import Roles
from bot.models import User
from bot.repositories.base import BaseRepository


class UserFilter(BaseModel):
    fullname: Optional[str] = None
    username: Optional[str] = None
    faculty: Optional[str] = None
    group: Optional[str] = None
    role: Optional[Roles] = None

    limit: Optional[int] = None
    offset: Optional[int] = None


class UserRepository(BaseRepository[User]):
    __model__ = User

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return (await self._session.scalars(
            select(self.__model__)
            .where(User.id == user_id)
            .options(joinedload("*"))
            .limit(1)
        )).first()

    async def find(self, user_filter: UserFilter) -> Sequence[User]:
        query = select(self.__model__).options(joinedload("*"))

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

        if user_filter.limit is not None:
            query = query.limit(user_filter.limit)
        if user_filter.offset is not None:
            query = query.offset(user_filter.offset)

        return (await self._session.scalars(query)).all()
