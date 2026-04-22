from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import ADMIN_ID
from app.database import queries as db
from app.keyboards.inline import center_selection_kb
from app.keyboards.reply import main_menu_kb
from app.states.registration import RegistrationState
from app.utils import texts

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    """Botni boshlash va ro'yxatdan o'tish."""
    await state.clear()
    user = await db.get_user(session, message.from_user.id)

    if user and user.learning_center:
        # Oldin ro'yxatdan o'tgan
        await message.answer(
            texts.WELCOME_BACK.format(name=user.full_name),
            reply_markup=main_menu_kb(is_admin=message.from_user.id == ADMIN_ID),
            parse_mode="HTML",
        )
        return

    await message.answer(texts.WELCOME, parse_mode="HTML")
    await state.set_state(RegistrationState.waiting_full_name)


@router.message(RegistrationState.waiting_full_name)
async def process_full_name(message: Message, state: FSMContext, session: AsyncSession):
    """Ism-familiyani qabul qilish."""
    full_name = message.text.strip()

    if len(full_name) < 3:
        await message.answer("⚠️ Iltimos, to'liq ism-familiyangizni kiriting (kamida 3 belgi):")
        return

    # Foydalanuvchini yaratish yoki yangilash
    user = await db.get_user(session, message.from_user.id)
    if not user:
        await db.add_user(session, message.from_user.id, full_name)
    
    await state.update_data(full_name=full_name)
    await message.answer(
        texts.ASK_CENTER,
        reply_markup=center_selection_kb(),
        parse_mode="HTML",
    )
    await state.set_state(RegistrationState.waiting_center)


@router.callback_query(RegistrationState.waiting_center, F.data.startswith("center:"))
async def process_center(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """O'quv markazini saqlash."""
    center = callback.data.split(":")[1]
    data = await state.get_data()
    full_name = data.get("full_name", "Foydalanuvchi")

    await db.update_user_center(session, callback.from_user.id, center)

    await callback.message.edit_text(
        texts.REGISTRATION_DONE.format(name=full_name, center=center),
        parse_mode="HTML",
    )
    await callback.message.answer(
        texts.MAIN_MENU,
        reply_markup=main_menu_kb(is_admin=callback.from_user.id == ADMIN_ID),
        parse_mode="HTML",
    )
    await state.clear()
    await callback.answer()
