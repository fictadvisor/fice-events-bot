from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.roles import Roles
from bot.repositories.user import UserRepository


class IsModerator(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery], session: AsyncSession) -> bool:
        if update.from_user is None:
            return False

        user_repository = UserRepository(session)
        user = await user_repository.get_by_id(update.from_user.id)
        if user is None:
            return False
        return user.role in (Roles.MODERATOR, Roles.ADMIN)

