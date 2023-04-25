from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.roles import Roles
from bot.keyboards.buttons import YES, NO
from bot.keyboards.confirm import CONFIRM_KEYBOARD
from bot.keyboards.register import REGISTER_KEYBOARD
from bot.messages.errors import INCORRECT_CONFIRM, USER_ALREADY_EXISTS
from bot.messages.start import START, START_FORM, INPUT_GROUP, INPUT_FACULTY, CONFIRM_INPUT, RESET_FORM, SUCCESS_FORM, \
    REGISTER
from bot.models import User
from bot.repositories.user import UserRepository
from bot.states.start_form import StartForm

start_router = Router()
start_router.message.filter(F.chat.type == ChatType.PRIVATE)


@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(message.chat.id)

    if user is not None:
        await message.answer(START)
        return

    await message.answer(START)
    await message.answer(REGISTER, reply_markup=REGISTER_KEYBOARD)


@start_router.callback_query(Text("register"))
async def register(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    if callback.message is None:
        return

    await state.clear()
    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(callback.from_user.id)
    if user is not None:
        await callback.message.edit_text(USER_ALREADY_EXISTS)
        return

    await callback.message.edit_text(START_FORM)
    await state.set_state(StartForm.fullname)


@start_router.message(StartForm.fullname)
async def input_fullname(message: Message, state: FSMContext) -> None:
    await state.update_data(fullname=message.text)
    await state.set_state(StartForm.faculty)
    await message.answer(INPUT_FACULTY)


@start_router.message(StartForm.faculty)
async def input_faculty(message: Message, state: FSMContext) -> None:
    await state.update_data(faculty=message.text)
    await state.set_state(StartForm.group)
    await message.answer(INPUT_GROUP)


@start_router.message(StartForm.group)
async def input_group(message: Message, state: FSMContext) -> None:
    data = await state.update_data(group=message.text)
    await state.set_state(StartForm.confirm)
    await message.answer(await CONFIRM_INPUT.render_async(
        fullname=data.get("fullname"),
        faculty=data.get("faculty"),
        group=data.get("group")
    ), reply_markup=CONFIRM_KEYBOARD)


@start_router.message(StartForm.confirm)
async def confirm_input(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if message.text not in [YES, NO]:
        await message.answer(INCORRECT_CONFIRM)
        return

    data = await state.get_data()
    await state.clear()
    if message.text == NO:
        await state.set_state(StartForm.fullname)
        await message.answer(RESET_FORM)
    else:
        user_repository = UserRepository(session)
        user = User(
            id=message.chat.id,
            fullname=data.get('fullname'),
            username=message.chat.username,
            faculty=data.get('faculty'),
            group=data.get('group'),
            role=Roles.USER
        )
        await user_repository.create(user)
        await message.answer(SUCCESS_FORM)
