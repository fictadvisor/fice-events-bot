from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from bot.models.base import Base

if TYPE_CHECKING:
    from bot.models.request import Request
    from bot.models.question import Question


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    date: Mapped[datetime]

    questions: Mapped[List["Question"]] = relationship(back_populates="event")
    requests: Mapped[List["Request"]] = relationship(back_populates="event")
