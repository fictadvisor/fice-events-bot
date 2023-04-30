from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.date_format import DATE_FORMAT
from bot.filters.is_moderaror import IsModerator
from bot.keyboards.inline.admin import get_events_keyboard, EventInfo, get_edit_keyboard, EditEvent, EditTargets, \
    get_questions_keyboard, QuestionInfo, get_question_keyboard, EditQuestion, EditTypes, AddQuestion
from bot.keyboards.inline.confirm import CONFIRM_KEYBOARD, ConfirmData, Select
from bot.messages.admin import ALL_EVENTS, EVENT_INFO, EDIT_TITLE, EDIT_DESCRIPTION, ALL_QUESTIONS, QUESTION_INFO, \
    EDIT_QUESTION, ADD_QUESTION, ADD_EVENT, INPUT_DESCRIPTION, CONFIRM_EVENT, INPUT_DATE, RESET_EVENT
from bot.messages.errors import INCORRECT_DATE_FORMAT
from bot.models import Question, Event
from bot.repositories.event import EventRepository
from bot.repositories.question import QuestionRepository, QuestionFilter
from bot.states.add_form import AddQuestionForm, AddEventForm
from bot.states.edit_form import EditForm

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
    ), reply_markup=await get_edit_keyboard(event.id))


@events_router.callback_query(EditEvent.filter(
    F.target == EditTargets.TITLE
))
async def start_edit_title(callback: CallbackQuery, state: FSMContext, callback_data: EditEvent) -> None:
    if callback.message is None:
        return

    await state.update_data(event_id=callback_data.event_id, message_id=callback.message.message_id)
    await state.set_state(EditForm.title)
    await callback.message.edit_text(EDIT_TITLE)


@events_router.message(EditForm.title)
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
        reply_markup=await get_edit_keyboard(event.id)
    )


@events_router.callback_query(EditEvent.filter(F.target == EditTargets.DESCRIPTION))
async def start_edit_description(callback: CallbackQuery, state: FSMContext, callback_data: EditEvent) -> None:
    if callback.message is None:
        return

    await state.update_data(event_id=callback_data.event_id, message_id=callback.message.message_id)
    await state.set_state(EditForm.description)
    await callback.message.edit_text(EDIT_DESCRIPTION)


@events_router.message(EditForm.description)
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
        reply_markup=await get_edit_keyboard(event.id)
    )


@events_router.callback_query(EditEvent.filter(F.target == EditTargets.QUESTIONS))
async def get_all_questions(callback: CallbackQuery, callback_data: EditEvent, session: AsyncSession) -> None:
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

    await callback.message.edit_text(await QUESTION_INFO.render_async(text=question.text), reply_markup=await get_question_keyboard(question.event_id, question.id))


@events_router.callback_query(EditQuestion.filter(F.type == EditTypes.EDIT))
async def start_edit_question(callback: CallbackQuery, state: FSMContext, callback_data: EditQuestion) -> None:
    if callback.message is None:
        return

    await state.update_data(question_id=callback_data.question_id, message_id=callback.message.message_id)
    await state.set_state(EditForm.question)
    await callback.message.edit_text(EDIT_QUESTION)


@events_router.message(EditForm.question)
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
        message_id=data.get("message_id"),
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
    await callback.message.edit_text(ALL_QUESTIONS, reply_markup=await get_questions_keyboard(question.event_id, questions))


@events_router.callback_query(AddQuestion.filter())
async def start_add_question(callback: CallbackQuery, state: FSMContext, callback_data: AddQuestion) -> None:
    if callback.message is None:
        return

    await state.update_data(event_id=callback_data.event_id, message_id=callback.message.message_id)
    await state.set_state(AddQuestionForm.question)
    await callback.message.edit_text(ADD_QUESTION)


@events_router.message(AddQuestionForm.question)
async def add_question(message: Message, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    await message.delete()

    data = await state.get_data()
    question_repository = QuestionRepository(session)
    question = Question(
        text=message.text or '',
        event_id=data.get("event_id", -1)
    )
    await question_repository.create(question)
    await session.flush()

    questions = await question_repository.find(QuestionFilter(event_id=data.get("event_id", -1)))

    await state.clear()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("message_id", -1),
        text=ALL_QUESTIONS,
        reply_markup=await get_questions_keyboard(data.get("event_id", -1), questions)
    )


@events_router.callback_query(Text("add_event"))
async def start_add_event(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message is None:
        return

    await state.update_data(message_id=callback.message.message_id)
    await state.set_state(AddEventForm.title)
    await callback.message.edit_text(ADD_EVENT)


@events_router.message(AddEventForm.title)
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


@events_router.message(AddEventForm.description)
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


@events_router.message(AddEventForm.date)
async def input_date(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.delete()

    data = await state.get_data()
    try:
        date = datetime.strptime(message.text or "", DATE_FORMAT)
    except ValueError as err:
        print(message.text, err)
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
async def confirm_event(callback: CallbackQuery, state: FSMContext, callback_data: ConfirmData, session: AsyncSession) -> None:
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


@events_router.callback_query(EditEvent.filter(F.target == EditTargets.DELETE))
async def delete_event(callback: CallbackQuery, callback_data: EditEvent, session: AsyncSession) -> None:
    if callback.message is None:
        return

    event_repository = EventRepository(session)
    await event_repository.delete(callback_data.event_id)

    events = await event_repository.get_all()

    await callback.message.edit_text(ALL_EVENTS, reply_markup=await get_events_keyboard(events))
