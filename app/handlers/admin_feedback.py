from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.database import queries as db
from app.utils import texts

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(F.text == "💬 Fikrlar")
async def show_feedbacks(message: Message, session: AsyncSession):
    """Barcha fikrlarni ko'rsatish."""
    feedbacks = await db.get_all_feedback(session)
    if not feedbacks:
        await message.answer(texts.ADMIN_NO_FEEDBACKS)
        return

    text = texts.ADMIN_FEEDBACKS_TITLE
    for fb in feedbacks[:20]:  # Oxirgi 20 ta
        user = fb.user
        status = "✅ O'qilgan" if fb.is_read else "🔴 Yangi"
        user_name = user.full_name if user else "Noma'lum"
        user_center = user.learning_center if user else "—"
        fb_date = fb.created_at.strftime('%d.%m.%Y %H:%M') if fb.created_at else ''
        text += (
            f"💬 <b>#{fb.id}</b>\n"
            f"👤 {user_name}\n"
            f"🏫 {user_center}\n"
            f"📅 {fb_date}\n"
            f"💬 {fb.message}\n"
            f"{status}\n"
            f"───────────────\n"
        )

        # O'qilgan deb belgilash
        if not fb.is_read:
            await db.mark_feedback_read(session, fb.id)

    await message.answer(text, parse_mode="HTML")
