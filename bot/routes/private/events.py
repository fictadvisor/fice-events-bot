from aiogram import Router
from aiogram.filters import Command, or_f, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.filters.is_registered import IsRegistered
from bot.keyboards.inline.confirm import CONFIRM_KEYBOARD, ConfirmData, Select
from bot.keyboards.inline.events import get_events_keyboard, SelectEvent, get_register_keyboard, RegisterEvent
from bot.keyboards.reply.buttons import EVENTS
from bot.messages.errors import REQUEST_ALREADY_EXISTS, REQUEST_NOT_CONFIRMED
from bot.messages.events import AVAILABLE_EVENTS, EVENT_INFO, SUCCESSFULLY_REGISTERED, START_REGISTRATION, \
    CONFIRM_REGISTRATION, RESET_REGISTRATION
from bot.models import Request, Answer
from bot.repositories.answer import AnswerRepository, AnswerFilter
from bot.repositories.event import EventRepository, EventFilter
from bot.repositories.question import QuestionRepository, QuestionFilter
from bot.repositories.request import RequestRepository, RequestFilter
from bot.states.registration_form import RegistrationForm

events_router = Router()
events_router.message.filter(IsRegistered())


@events_router.message(or_f(Text(EVENTS), Command("events")))
async def see_events(message: Message, session: AsyncSession) -> None:
    events_repository = EventRepository(session)
    events = await events_repository.find(EventFilter(ended=False))
    await message.answer(AVAILABLE_EVENTS, reply_markup=await get_events_keyboard(events))


@events_router.callback_query(SelectEvent.filter())
async def select_event(callback: CallbackQuery, callback_data: SelectEvent, session: AsyncSession) -> None:
    if callback.message is None:
        return

    events_repository = EventRepository(session)
    event = await events_repository.get_by_id(callback_data.event_id)
    if event is None:
        return

    request_repository = RequestRepository(session)
    request = await request_repository.find_one(RequestFilter(
        user_id=callback.from_user.id,
        event_id=callback_data.event_id
    ))

    reply_markup = None
    if request is None or not request.confirmed:
        reply_markup = await get_register_keyboard(event_id=event.id)

    await callback.message.edit_text(await EVENT_INFO.render_async(
        title=event.title,
        description=event.description,
        date=event.date
    ), reply_markup=reply_markup)


@events_router.callback_query(RegisterEvent.filter())
async def register_event(callback: CallbackQuery, state: FSMContext, callback_data: RegisterEvent,
                         session: AsyncSession) -> None:
    if callback.message is None:
        return

    request_repository = RequestRepository(session)
    request = await request_repository.find_one(RequestFilter(
        user_id=callback.from_user.id,
        event_id=callback_data.event_id
    ))

    if request is not None:
        if request.confirmed:
            await callback.message.edit_text(REQUEST_ALREADY_EXISTS)
        else:
            await state.set_state(RegistrationForm.form)
            await state.update_data(
                event_id=callback_data.event_id,
                request_id=request.id
            )
            await callback.message.edit_text(REQUEST_NOT_CONFIRMED, reply_markup=CONFIRM_KEYBOARD)
        return

    request = Request(
        user_id=callback.from_user.id,
        event_id=callback_data.event_id
    )
    await request_repository.create(request)
    await session.flush()

    question_repository = QuestionRepository(session)
    questions = await question_repository.find(QuestionFilter(event_id=callback_data.event_id))

    if len(questions) == 0:
        request.confirmed = True
        await callback.message.edit_text(SUCCESSFULLY_REGISTERED)
        return
    await state.update_data(
        offset=1,
        event_id=callback_data.event_id,
        request_id=request.id
    )
    await callback.message.edit_text(START_REGISTRATION)
    await callback.message.answer(questions[0].text)
    await state.set_state(RegistrationForm.form)


@events_router.callback_query(RegistrationForm.form, ConfirmData.filter())
async def reset_form(callback: CallbackQuery, state: FSMContext, callback_data: ConfirmData,
                     session: AsyncSession) -> None:
    if callback.message is None:
        return

    data = await state.get_data()
    question_repository = QuestionRepository(session)
    answer_repository = AnswerRepository(session)
    if callback_data.select == Select.YES:
        answers = await answer_repository.find(AnswerFilter(request_id=data.get("request_id", -1)),
                                               options=(selectinload(Answer.question),))
        question = await question_repository.find_one(QuestionFilter(event_id=data.get("event_id", -1)),
                                                      offset=len(answers))
        if question is None:
            await state.set_state(RegistrationForm.confirm)
            await callback.message.edit_text(await CONFIRM_REGISTRATION.render_async(answers=answers),
                                             reply_markup=CONFIRM_KEYBOARD)
            return

        await state.update_data(offset=len(answers) + 1)
        await callback.message.edit_text(question.text)
    else:
        await answer_repository.delete_many(AnswerFilter(request_id=data.get("request_id", -1)))
        question = await question_repository.find_one(QuestionFilter(event_id=data.get("event_id", -1)))
        if question is None:
            return

        await state.update_data(offset=1)
        await callback.message.edit_text(question.text)


@events_router.message(RegistrationForm.form)
async def answer_question(message: Message, state: FSMContext, session: AsyncSession) -> None:
    data = await state.get_data()
    offset = data.get("offset", 1)

    question_repository = QuestionRepository(session)
    previous_question = await question_repository.find_one(
        QuestionFilter(event_id=data.get('event_id', -1)),
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
        QuestionFilter(event_id=data.get("event_id", -1)),
        offset=data.get("offset")
    )
    if question is None:
        answers = await answer_repository.find(
            AnswerFilter(request_id=data.get("request_id", -1)),
            options=(
                selectinload(Answer.question),
            )
        )
        await state.set_state(RegistrationForm.confirm)
        await message.answer(await CONFIRM_REGISTRATION.render_async(answers=answers), reply_markup=CONFIRM_KEYBOARD)
    else:
        await state.update_data(offset=offset + 1)
        await message.answer(question.text)


@events_router.callback_query(RegistrationForm.confirm, ConfirmData.filter())
async def confirm_registration(callback: CallbackQuery, state: FSMContext, callback_data: ConfirmData,
                               session: AsyncSession) -> None:
    if callback.message is None:
        return

    data = await state.get_data()

    request_repository = RequestRepository(session)
    request = await request_repository.find_one(
        RequestFilter(user_id=callback.from_user.id, event_id=data.get("event_id", -1), confirmed=False))
    if request is None:
        return

    if callback_data.select == Select.YES:
        request.confirmed = True
        await callback.message.edit_text(SUCCESSFULLY_REGISTERED)
        await state.clear()
        return
    else:
        answer_repository = AnswerRepository(session)
        await answer_repository.delete_many(AnswerFilter(request_id=data.get("request_id", -1)))

        await callback.message.edit_text(RESET_REGISTRATION)

        question_repository = QuestionRepository(session)
        question = await question_repository.find_one(QuestionFilter(event_id=data.get("event_id", -1)))
        if question is None:
            return
        await callback.message.answer(question.text)
        await state.update_data(offset=1)
        await state.set_state(RegistrationForm.form)
