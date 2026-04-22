from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import queries as db
from app.keyboards.inline import favorites_kb
from app.utils import texts

router = Router()


@router.message(F.text == "⭐ Sevimlilar")
async def show_favorites(message: Message, session: AsyncSession):
    """Sevimlilar ro'yxatini ko'rsatish."""
    favs = await db.get_favorites(session, message.from_user.id)
    if not favs:
        await message.answer(texts.NO_FAVORITES)
        return

    await message.answer(
        texts.FAVORITES_TITLE,
        reply_markup=favorites_kb(favs),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("fav:"))
async def toggle_favorite(callback: CallbackQuery, session: AsyncSession):
    """Sevimlilarga qo'shish/o'chirish."""
    resource_id = int(callback.data.split(":")[1])
    is_fav = await db.is_favorite(session, callback.from_user.id, resource_id)

    if is_fav:
        await db.remove_favorite(session, callback.from_user.id, resource_id)
        await callback.answer(texts.REMOVED_FROM_FAVORITES, show_alert=True)
    else:
        await db.add_favorite(session, callback.from_user.id, resource_id)
        await callback.answer(texts.ADDED_TO_FAVORITES, show_alert=True)
