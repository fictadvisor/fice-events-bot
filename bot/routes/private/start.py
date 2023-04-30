from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.roles import Roles
from bot.keyboards.inline.confirm import CONFIRM_KEYBOARD, ConfirmData, Select
from bot.keyboards.inline.register import REGISTER_KEYBOARD
from bot.keyboards.reply.start_menu import get_start_menu
from bot.messages.errors import USER_ALREADY_EXISTS
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

    reply_markup = None
    if user is not None:
        reply_markup = await get_start_menu(user.role in (Roles.MODERATOR, Roles.ADMIN))

    await message.answer(START, reply_markup=reply_markup)
    if user is None:
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


@start_router.callback_query(StartForm.confirm, ConfirmData.filter())
async def confirm_input(callback: CallbackQuery, callback_data: ConfirmData, state: FSMContext,
                        session: AsyncSession) -> None:
    if callback.message is None:
        return

    data = await state.get_data()
    await state.clear()
    if callback_data.select == Select.NO:
        await state.set_state(StartForm.fullname)
        await callback.message.edit_text(RESET_FORM)
    else:
        user_repository = UserRepository(session)
        user = User(
            id=callback.from_user.id,
            fullname=data.get('fullname'),
            username=callback.from_user.username,
            faculty=data.get('faculty'),
            group=data.get('group'),
            role=Roles.USER
        )
        await user_repository.create(user)
        await callback.message.edit_text(SUCCESS_FORM)
