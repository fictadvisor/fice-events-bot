from datetime import datetime
from io import BytesIO

import pandas as pd
from aiogram import Router, F, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.constants.date_format import DATE_FORMAT
from bot.constants.request_types import RequestTypes
from bot.filters.is_moderaror import IsModerator
from bot.keyboards.inline.admin import get_events_keyboard, EventInfo, get_event_keyboard, EventAction, EventActions, \
    get_questions_keyboard, QuestionInfo, get_question_keyboard, EditQuestion, EditTypes, AddQuestion, get_edit_keyboard
from bot.keyboards.inline.confirm import CONFIRM_KEYBOARD, ConfirmData, Select
from bot.messages.admin import ALL_EVENTS, EVENT_INFO, EDIT_TITLE, EDIT_DESCRIPTION, ALL_QUESTIONS, QUESTION_INFO, \
    EDIT_QUESTION, ADD_QUESTION, ADD_EVENT, INPUT_DESCRIPTION, CONFIRM_EVENT, INPUT_DATE, RESET_EVENT, EDIT_DATE, \
    SEND_MESSAGE
from bot.messages.errors import INCORRECT_DATE_FORMAT
from bot.models import Question, Event, User, Answer, Request
from bot.repositories.event import EventRepository
from bot.repositories.question import QuestionRepository, QuestionFilter
from bot.states.add_form import AddQuestionForm, AddEventForm
from bot.states.edit_form import EditForm
from bot.states.send_form import SendForm

events_router = Router()
events_router.message.filter(IsModerator())
events_router.callback_query.filter(IsModerator())


@events_router.callback_query(Text("admin:events"))
async def get_events(callback: CallbackQuery, session: AsyncSession) -> None:
    if callback.message is None:
        return

    event_repository = EventRepository(session)
    events = await event_repository.get_all()

    await callback.message.edit_text(ALL_EVENTS, reply_markup=await get_events_keyboard(events))


@events_router.callback_query(EventInfo.filter())
async def get_event(callback: CallbackQuery, callback_data: EventInfo, session: AsyncSession) -> None:
    if callback.message is None:
        return

    event_repository = EventRepository(session)
    event = await event_repository.get_by_id(callback_data.event_id)
    if event is None:
        return

    await callback.message.edit_text(await EVENT_INFO.render_async(
        title=event.title,
        description=event.description,
        date=event.date
    ), reply_markup=await get_event_keyboard(event.id, event.published))


@events_router.callback_query(EventAction.filter(
    F.action == EventActions.EDIT
))
async def edit_event(callback: CallbackQuery, callback_data: EventAction, session: AsyncSession) -> None:
    if callback.message is None:
        return

    event_repository = EventRepository(session)
    event = await event_repository.get_by_id(callback_data.event_id)
    if event is None:
        return

    await callback.message.edit_text(await EVENT_INFO.render_async(
        title=event.title,
        description=event.description,
        date=event.date
    ), reply_markup=await get_edit_keyboard(event.id))


@events_router.callback_query(EventAction.filter(
    F.action == EventActions.TITLE
))
async def start_edit_title(callback: CallbackQuery, state: FSMContext, callback_data: EventAction) -> None:
    if callback.message is None:
        return

    await state.update_data(event_id=callback_data.event_id, message_id=callback.message.message_id)
    await state.set_state(EditForm.title)
    await callback.message.edit_text(EDIT_TITLE)


@events_router.message(EditForm.title, F.text)
async def edit_title(message: Message, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    await message.delete()

    data = await state.get_data()

    event_repository = EventRepository(session)
    event = await event_repository.get_by_id(data.get("event_id", -1))
    if event is None:
        return

    event.title = message.text or ''

    await state.clear()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("message_id"),
        text=await EVENT_INFO.render_async(
            title=event.title,
            description=event.description,
            date=event.date
        ),
        reply_markup=await get_event_keyboard(event.id, event.published)
    )


@events_router.callback_query(EventAction.filter(F.action == EventActions.DESCRIPTION))
async def start_edit_description(callback: CallbackQuery, state: FSMContext, callback_data: EventAction) -> None:
    if callback.message is None:
        return

    await state.update_data(event_id=callback_data.event_id, message_id=callback.message.message_id)
    await state.set_state(EditForm.description)
    await callback.message.edit_text(EDIT_DESCRIPTION)


@events_router.message(EditForm.description, F.text)
async def edit_description(message: Message, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    await message.delete()

    data = await state.get_data()

    event_repository = EventRepository(session)
    event = await event_repository.get_by_id(data.get("event_id", -1))
    if event is None:
        return

    event.description = message.text or ''

    await state.clear()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("message_id"),
        text=await EVENT_INFO.render_async(
            title=event.title,
            description=event.description,
            date=event.date
        ),
        reply_markup=await get_event_keyboard(event.id, event.published)
    )


@events_router.callback_query(EventAction.filter(F.action == EventActions.DATE))
async def start_edit_date(callback: CallbackQuery, state: FSMContext, callback_data: EventAction) -> None:
    if callback.message is None:
        return

    await state.update_data(event_id=callback_data.event_id, message_id=callback.message.message_id)
    await state.set_state(EditForm.date)
    await callback.message.edit_text(EDIT_DATE)


@events_router.message(EditForm.date, F.text)
async def edit_date(message: Message, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    await message.delete()

    data = await state.get_data()

    try:
        date = datetime.strptime(message.text or "", DATE_FORMAT)
    except ValueError:
        if message.text != INCORRECT_DATE_FORMAT:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data.get("message_id", -1),
                text=INCORRECT_DATE_FORMAT
            )
        return

    event_repository = EventRepository(session)
    event = await event_repository.get_by_id(data.get("event_id", -1))
    if event is None:
        return

    event.date = date

    await state.clear()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("message_id", -1),
        text=await EVENT_INFO.render_async(
            title=event.title,
            description=event.description,
            date=event.date
        ),
        reply_markup=await get_event_keyboard(event.id, event.published)
    )


@events_router.callback_query(EventAction.filter(F.action == EventActions.QUESTIONS))
async def get_all_questions(callback: CallbackQuery, callback_data: EventAction, session: AsyncSession) -> None:
    if callback.message is None:
        return

    question_repository = QuestionRepository(session)
    questions = await question_repository.find(QuestionFilter(event_id=callback_data.event_id))

    await callback.message.edit_text(
        ALL_QUESTIONS,
        reply_markup=await get_questions_keyboard(callback_data.event_id, questions)
    )


@events_router.callback_query(QuestionInfo.filter())
async def question_info(callback: CallbackQuery, callback_data: QuestionInfo, session: AsyncSession) -> None:
    if callback.message is None:
        return

    question_repository = QuestionRepository(session)
    question = await question_repository.get_by_id(callback_data.question_id)
    if question is None:
        return

    await callback.message.edit_text(await QUESTION_INFO.render_async(text=question.text),
                                     reply_markup=await get_question_keyboard(question.event_id, question.id))


@events_router.callback_query(EditQuestion.filter(F.type == EditTypes.EDIT))
async def start_edit_question(callback: CallbackQuery, state: FSMContext, callback_data: EditQuestion) -> None:
    if callback.message is None:
        return

    await state.update_data(question_id=callback_data.question_id, message_id=callback.message.message_id)
    await state.set_state(EditForm.question)
    await callback.message.edit_text(EDIT_QUESTION)


@events_router.message(EditForm.question, F.text)
async def edit_question(message: Message, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    await message.delete()

    data = await state.get_data()

    question_repository = QuestionRepository(session)
    question = await question_repository.get_by_id(data.get("question_id", -1))
    if question is None:
        return

    question.text = message.text or ''

    await state.clear()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("message_id", -1),
        text=await QUESTION_INFO.render_async(text=question.text),
        reply_markup=await get_question_keyboard(question.event_id, question.id)
    )


@events_router.callback_query(EditQuestion.filter(F.type == EditTypes.DELETE))
async def delete_question(callback: CallbackQuery, callback_data: EditQuestion, session: AsyncSession) -> None:
    if callback.message is None:
        return

    question_repository = QuestionRepository(session)
    question = await question_repository.get_by_id(callback_data.question_id)
    if question is None:
        return
    await question_repository.delete(callback_data.question_id)

    questions = await question_repository.find(QuestionFilter(event_id=question.event_id))
    await callback.message.edit_text(ALL_QUESTIONS,
                                     reply_markup=await get_questions_keyboard(question.event_id, questions))


@events_router.callback_query(AddQuestion.filter())
async def start_add_question(callback: CallbackQuery, state: FSMContext, callback_data: AddQuestion) -> None:
    if callback.message is None:
        return

    await state.update_data(event_id=callback_data.event_id, message_id=callback.message.message_id,
                            question_type=callback_data.type)
    await state.set_state(AddQuestionForm.question)
    await callback.message.edit_text(ADD_QUESTION)


@events_router.message(AddQuestionForm.question, F.text)
async def add_question(message: Message, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    await message.delete()

    data = await state.get_data()
    question_repository = QuestionRepository(session)
    question = Question(
        text=message.text or '',
        event_id=data.get("event_id", -1),
        type=data.get("question_type", RequestTypes.REGISTER)
    )
    await question_repository.create(question)
    await session.flush()

    questions = await question_repository.find(QuestionFilter(event_id=data.get("event_id", -1), type=data.get("question_type", RequestTypes.REGISTER)))

    await state.clear()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("message_id", -1),
        text=ALL_QUESTIONS,
        reply_markup=await get_questions_keyboard(data.get("event_id", -1), questions, request_type=data.get("question_type", RequestTypes.REGISTER))
    )


@events_router.callback_query(Text("add_event"))
async def start_add_event(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message is None:
        return

    await state.update_data(message_id=callback.message.message_id)
    await state.set_state(AddEventForm.title)
    await callback.message.edit_text(ADD_EVENT)


@events_router.message(AddEventForm.title, F.text)
async def input_title(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.delete()

    data = await state.get_data()

    await state.set_state(AddEventForm.description)
    await state.update_data(title=message.text or '')
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("message_id", -1),
        text=INPUT_DESCRIPTION
    )


@events_router.message(AddEventForm.description, F.text)
async def input_description(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.delete()

    data = await state.get_data()

    await state.set_state(AddEventForm.date)
    await state.update_data(description=message.text or '')
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("message_id", -1),
        text=INPUT_DATE
    )


@events_router.message(AddEventForm.date, F.text)
async def input_date(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.delete()

    data = await state.get_data()
    try:
        date = datetime.strptime(message.text or "", DATE_FORMAT)
    except ValueError:
        if message.text != INCORRECT_DATE_FORMAT:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data.get("message_id", -1),
                text=INCORRECT_DATE_FORMAT
            )
        return

    await state.update_data(date=date.strftime(DATE_FORMAT))
    await state.set_state(AddEventForm.confirm)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("message_id", -1),
        text=await CONFIRM_EVENT.render_async(
            title=data.get("title", ""),
            description=data.get("description", ""),
            date=date
        ),
        reply_markup=CONFIRM_KEYBOARD
    )


@events_router.callback_query(AddEventForm.confirm, ConfirmData.filter())
async def confirm_event(callback: CallbackQuery, state: FSMContext, callback_data: ConfirmData,
                        session: AsyncSession) -> None:
    if callback.message is None:
        return

    if callback_data.select == Select.YES:
        data = await state.get_data()

        event_repository = EventRepository(session)
        event = Event(
            title=data.get("title", ""),
            description=data.get("description", ""),
            date=datetime.strptime(data.get("date", ""), DATE_FORMAT)
        )
        await event_repository.create(event)
        await session.flush()

        events = await event_repository.get_all()

        await callback.message.edit_text(ALL_EVENTS, reply_markup=await get_events_keyboard(events))
    else:
        await state.clear()
        await state.update_data(message_id=callback.message.message_id)
        await state.set_state(AddEventForm.title)
        await callback.message.edit_text(RESET_EVENT)


@events_router.callback_query(EventAction.filter(F.action == EventActions.DELETE))
async def delete_event(callback: CallbackQuery, callback_data: EventAction, session: AsyncSession) -> None:
    if callback.message is None:
        return

    event_repository = EventRepository(session)
    await event_repository.delete(callback_data.event_id)

    events = await event_repository.get_all()

    await callback.message.edit_text(ALL_EVENTS, reply_markup=await get_events_keyboard(events))


@events_router.callback_query(EventAction.filter(F.action == EventActions.EXPORT))
async def export_requests(callback: CallbackQuery, callback_data: EventAction, session: AsyncSession) -> None:
    if callback.message is None:
        return

    event_repository = EventRepository(session)
    event = await event_repository.get_by_id(callback_data.event_id)
    if event is None:
        return

    data = (await session.execute(
        select(
            User.fullname.label("fullname"),
            User.username.label("username"),
            User.faculty.label("faculty"),
            User.group.label("group"),
            Question.text.label("question"),
            Answer.text.label("answer")
        )
        .select_from(Request)
        .join(User, Request.user_id == User.id, isouter=True)
        .join(Question, Request.event_id == Question.event_id, isouter=True)
        .join(Answer, and_(Request.id == Answer.request_id, Question.id == Answer.question_id), isouter=True)
        .order_by(User.id.desc(), Question.id)
        .where(Request.event_id == event.id)
    )).all()

    bio = BytesIO()

    df = pd.DataFrame(list(data))
    with pd.ExcelWriter(bio, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=event.title)
    await callback.message.answer_document(BufferedInputFile(bio.getvalue(), filename=f"{event.title}.xlsx"))


@events_router.callback_query(EventAction.filter(F.action == EventActions.PUBLISH))
async def publish_event(callback: CallbackQuery, callback_data: EventAction, session: AsyncSession) -> None:
    if callback.message is None:
        return

    event_repository = EventRepository(session)
    event = await event_repository.get_by_id(callback_data.event_id)
    if event is None:
        return

    event.published = not event.published

    await callback.message.edit_text(
        text=await EVENT_INFO.render_async(
            title=event.title,
            description=event.description,
            date=event.date
        ),
        reply_markup=await get_event_keyboard(event.id, event.published)
    )


@events_router.callback_query(EventAction.filter(F.action == EventActions.SEND))
async def send_form(callback: CallbackQuery, state: FSMContext, callback_data: EventAction) -> None:
    if callback.message is None:
        return

    await state.set_state(SendForm.form)
    await state.update_data(event_id=callback_data.event_id, message_id=callback.message.message_id)

    await callback.message.edit_text(SEND_MESSAGE)


@events_router.message(SendForm.form)
async def send_message(message: Message, state: FSMContext, bot: Bot, session: AsyncSession) -> None:
    text = message.html_text
    await message.delete()

    data = await state.get_data()

    event_repository = EventRepository(session)
    event = await event_repository.get_by_id(data.get("event_id", -1), options=[
        selectinload(Event.requests).subqueryload(Request.user)
    ])
    if event is None:
        return
    for request in event.requests:
        try:
            await bot.send_message(request.user_id, text)
        except:
            pass

    await state.clear()
    await bot.edit_message_text(
        text=await EVENT_INFO.render_async(
            title=event.title,
            description=event.description,
            date=event.date
        ),
        chat_id=message.chat.id,
        message_id=data.get("message_id", -1),
        reply_markup=await get_event_keyboard(event.id, event.published)
    )


@events_router.callback_query(EventAction.filter(F.action == EventActions.FEEDBACK))
async def get_feedback(callback: CallbackQuery, callback_data: EventAction, session: AsyncSession) -> None:
    if callback.message is None:
        return

    question_repository = QuestionRepository(session)
    questions = await question_repository.find(
        QuestionFilter(event_id=callback_data.event_id, type=RequestTypes.FEEDBACK))

    await callback.message.edit_text(
        ALL_QUESTIONS,
        reply_markup=await get_questions_keyboard(callback_data.event_id, questions, RequestTypes.FEEDBACK)
    )
