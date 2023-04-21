from typing import Generic, TypeVar, Sequence, Optional, Type, Any
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    __model__: Type[T]

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, model: T) -> T:
        self._session.add(model)
        return model

    async def get_all(self) -> Sequence[T]:
        query = select(self.__model__)
        return (await self._session.scalars(query)).all()

    async def get_by_id(self, model_id: int) -> Optional[T]:
        return await self._session.get(self.__model__, model_id)

    async def update(self, model_id: int, **kwargs: Any) -> None:
        query = update(self.__model__) \
            .filter_by(id=model_id) \
            .values(**kwargs) \
            .execution_options(synchronize_session="evaluate")
        await self._session.execute(query)

    async def delete(self, model_id: int) -> None:
        query = delete(self.__model__).filter_by(id=model_id)
        await self._session.execute(query)
