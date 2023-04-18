from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import Base

if TYPE_CHECKING:
    from bot.models.request import Request
    from bot.models.question import Question


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]

    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"))
    request: Mapped["Request"] = relationship(back_populates="answers")
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    question: Mapped["Question"] = relationship(back_populates="answers")
