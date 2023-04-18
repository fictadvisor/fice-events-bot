from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import Base

if TYPE_CHECKING:
    from bot.models.event import Event
    from bot.models.answer import Answer


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]

    answers: Mapped[List["Answer"]] = relationship(back_populates="question")

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship(back_populates="questions")
