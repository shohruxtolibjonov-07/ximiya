from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import ADMIN_ID
from app.database import queries as db
from app.keyboards.reply import cancel_kb, main_menu_kb
from app.states.feedback import FeedbackState
from app.utils import texts

router = Router()


@router.message(F.text == "💬 Fikr bildirish")
async def feedback_prompt(message: Message, state: FSMContext):
    """Fikr bildirish rejimini boshlash."""
    await message.answer(
        texts.FEEDBACK_PROMPT,
        reply_markup=cancel_kb(),
    )
    await state.set_state(FeedbackState.waiting_message)


@router.message(FeedbackState.waiting_message, F.text == "❌ Bekor qilish")
async def cancel_feedback(message: Message, state: FSMContext):
    """Fikr bildirishni bekor qilish."""
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=main_menu_kb(is_admin=message.from_user.id == ADMIN_ID))


@router.message(FeedbackState.waiting_message)
async def process_feedback(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    """Fikrni qabul qilish va saqlash."""
    if not message.text:
        await message.answer("⚠️ Iltimos, matn yozing.")
        return

    feedback_text = message.text.strip()
    if len(feedback_text) < 5:
        await message.answer("⚠️ Iltimos, kamida 5 belgi kiriting.")
        return

    await db.add_feedback(session, message.from_user.id, feedback_text)

    await message.answer(
        texts.FEEDBACK_SENT,
        reply_markup=main_menu_kb(is_admin=message.from_user.id == ADMIN_ID),
    )
    await state.clear()

    # Adminga xabar yuborish
    user = await db.get_user(session, message.from_user.id)
    try:
        await bot.send_message(
            ADMIN_ID,
            texts.FEEDBACK_RECEIVED.format(
                name=user.full_name if user else "Noma'lum",
                user_id=message.from_user.id,
                center=user.learning_center if user else "Noma'lum",
                message=feedback_text,
            ),
            parse_mode="HTML",
        )
    except Exception:
        pass
