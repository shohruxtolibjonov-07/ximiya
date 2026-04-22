import logging
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import queries as db
from app.database.engine import async_session

logger = logging.getLogger(__name__)


async def notify_all_users(bot: Bot, text: str, exclude_id: int = None):
    """Barcha foydalanuvchilarga xabar yuborish."""
    async with async_session() as session:
        users = await db.get_all_users(session)
        success = 0
        for user in users:
            if exclude_id and user.telegram_id == exclude_id:
                continue
            try:
                await bot.send_message(user.telegram_id, text, parse_mode="HTML")
                success += 1
            except Exception as e:
                logger.warning(f"Xabar yuborib bo'lmadi {user.telegram_id}: {e}")
        return success


async def notify_new_resource(bot: Bot, title: str, admin_id: int):
    """Yangi resurs haqida xabar."""
    text = f"📢 <b>Yangi resurs qo'shildi!</b>\n\n📄 {title}\n\n📚 Resurslar bo'limidan ko'ring!"
    return await notify_all_users(bot, text, exclude_id=admin_id)


async def notify_new_quiz(bot: Bot, title: str, admin_id: int):
    """Yangi test haqida xabar."""
    text = f"📢 <b>Yangi test qo'shildi!</b>\n\n📝 {title}\n\n📝 Testlar bo'limidan boshlang!"
    return await notify_all_users(bot, text, exclude_id=admin_id)
