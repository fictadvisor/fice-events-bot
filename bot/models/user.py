from typing import List, TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.constants.roles import Roles
from bot.models.base import Base

if TYPE_CHECKING:
    from bot.models.request import Request


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fullname: Mapped[str]
    username: Mapped[str]
    faculty: Mapped[str]
    group: Mapped[str]
    role: Mapped[Roles]

    requests: Mapped[List["Request"]] = relationship(back_populates="user")
