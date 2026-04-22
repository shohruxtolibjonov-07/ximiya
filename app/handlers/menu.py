from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import ADMIN_ID
from app.database import queries as db
from app.keyboards.reply import main_menu_kb, admin_menu_kb
from app.utils import texts

router = Router()


@router.message(F.text == "⚙️ Admin panel")
async def admin_panel_button(message: Message, state: FSMContext):
    """Admin panel tugmasi (asosiy menyudan)."""
    if message.from_user.id != ADMIN_ID:
        await message.answer(texts.ADMIN_ONLY)
        return
    await state.clear()
    await message.answer(texts.ADMIN_MENU, reply_markup=admin_menu_kb(), parse_mode="HTML")


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    """Admin panel komandasi."""
    if message.from_user.id != ADMIN_ID:
        await message.answer(texts.ADMIN_ONLY)
        return
    await state.clear()
    await message.answer(texts.ADMIN_MENU, reply_markup=admin_menu_kb(), parse_mode="HTML")


@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main_menu(message: Message, state: FSMContext):
    """Asosiy menyuga qaytish."""
    await state.clear()
    await message.answer(
        texts.MAIN_MENU,
        reply_markup=main_menu_kb(is_admin=message.from_user.id == ADMIN_ID),
        parse_mode="HTML",
    )



@router.message(F.text == "💡 Kunlik maslahat")
async def daily_tip(message: Message, session: AsyncSession):
    """Kunlik kimyo maslahati ko'rsatish."""
    tip = await db.get_random_tip(session)
    if tip:
        await message.answer(
            texts.DAILY_TIP.format(tip=tip.tip_text),
            parse_mode="HTML",
        )
    else:
        await message.answer(texts.NO_TIPS)


@router.message(F.text == "🏆 Reyting")
async def show_leaderboard(message: Message, session: AsyncSession):
    """Reyting jadvalini ko'rsatish."""
    leaders = await db.get_leaderboard(session)
    if not leaders:
        await message.answer(texts.LEADERBOARD_EMPTY)
        return

    medals = ["🥇", "🥈", "🥉"]
    text = texts.LEADERBOARD_TITLE
    for i, row in enumerate(leaders):
        medal = medals[i] if i < 3 else "  "
        pct = round((row.total_score / row.total_questions) * 100, 1) if row.total_questions else 0
        text += texts.LEADERBOARD_ROW.format(
            rank=i + 1,
            medal=medal,
            name=row.full_name,
            score=row.total_score,
            total=row.total_questions,
            pct=pct,
        )

    await message.answer(text, parse_mode="HTML")


@router.message(F.text == "📊 Mening natijalarim")
async def show_my_progress(message: Message, session: AsyncSession):
    """Foydalanuvchi progressini ko'rsatish."""
    progress = await db.get_user_progress(session, message.from_user.id)
    await message.answer(
        texts.USER_PROGRESS.format(
            tests=progress["tests_taken"],
            score=progress["total_score"],
            total=progress["total_questions"],
            pct=progress["percentage"],
        ),
        parse_mode="HTML",
    )
