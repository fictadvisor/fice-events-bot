from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import Base

if TYPE_CHECKING:
    from bot.models.user import User
    from bot.models.event import Event
    from bot.models.answer import Answer


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    confirmed: Mapped[bool] = mapped_column(default=False)

    answers: Mapped[List["Answer"]] = relationship(back_populates="request", cascade="all, delete", passive_deletes=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="requests")
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    event: Mapped["Event"] = relationship(back_populates="requests")

    __table_args__ = (
        UniqueConstraint(user_id, event_id),
    )
