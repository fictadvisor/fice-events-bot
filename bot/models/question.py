from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.constants.request_types import RequestTypes
from bot.models.base import Base

if TYPE_CHECKING:
    from bot.models.event import Event
    from bot.models.answer import Answer


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    type: Mapped[RequestTypes] = mapped_column(default=RequestTypes.REGISTER)

    answers: Mapped[List["Answer"]] = relationship("Answer", back_populates="question", cascade="all, delete", passive_deletes=True)

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    event: Mapped["Event"] = relationship("Event", back_populates="questions")
