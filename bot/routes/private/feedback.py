from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.request_types import RequestTypes
from bot.filters.is_registered import IsRegistered
from bot.keyboards.inline.events import RegisterEvent
from bot.keyboards.inline.feedback import FeedbackEvent
from bot.messages.feedback import SUCCESSFULLY_FEEDBACK
from bot.models import Request, Answer
from bot.repositories.answer import AnswerRepository
from bot.repositories.question import QuestionRepository, QuestionFilter
from bot.repositories.request import RequestRepository, RequestFilter
from bot.states.feedback_form import FeedbackForm

feedback_router = Router()
feedback_router.message.filter(IsRegistered())


@feedback_router.callback_query(FeedbackEvent.filter())
async def feedback_event(callback: CallbackQuery, state: FSMContext, callback_data: RegisterEvent,
                         session: AsyncSession) -> None:
    if callback.message is None:
        return

    request_repository = RequestRepository(session)

    request = Request(
        user_id=callback.from_user.id,
        event_id=callback_data.event_id,
        type=RequestTypes.FEEDBACK
    )
    await request_repository.create(request)
    await session.flush()

    question_repository = QuestionRepository(session)
    questions = await question_repository.find(
        QuestionFilter(event_id=callback_data.event_id, type=RequestTypes.FEEDBACK))

    if len(questions) == 0:
        request.confirmed = True
        await callback.message.edit_text(SUCCESSFULLY_FEEDBACK)
        return
    await state.update_data(
        offset=1,
        event_id=callback_data.event_id,
        request_id=request.id
    )
    await callback.message.edit_reply_markup()
    await callback.message.answer(questions[0].text)
    await state.set_state(FeedbackForm.form)


@feedback_router.message(F.text, FeedbackForm.form)
async def answer_question(message: Message, state: FSMContext, session: AsyncSession) -> None:
    data = await state.get_data()
    offset = data.get("offset", 1)

    question_repository = QuestionRepository(session)
    previous_question = await question_repository.find_one(
        QuestionFilter(event_id=data.get('event_id', -1), type=RequestTypes.FEEDBACK),
        offset=offset - 1
    )
    if previous_question is None:
        return

    answer = Answer(
        text=message.text,
        request_id=data.get("request_id", -1),
        question_id=previous_question.id
    )
    answer_repository = AnswerRepository(session)
    await answer_repository.create(answer)
    await session.flush()

    question = await question_repository.find_one(
        QuestionFilter(event_id=data.get("event_id", -1), type=RequestTypes.FEEDBACK),
        offset=data.get("offset")
    )
    if question is None:
        request_repository = RequestRepository(session)
        request = await request_repository.find_one(
            RequestFilter(user_id=message.from_user.id, event_id=data.get("event_id", -1), type=RequestTypes.FEEDBACK))
        if request is None:
            return
        request.confirmed = True

        await state.clear()
        await message.answer(SUCCESSFULLY_FEEDBACK)
    else:
        await state.update_data(offset=offset + 1)
        await message.answer(question.text)
