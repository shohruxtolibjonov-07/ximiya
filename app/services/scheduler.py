import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot

from app.database import queries as db
from app.database.engine import async_session
from app.utils import texts

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")


async def send_daily_tip(bot: Bot):
    """Kunlik kimyo maslahatini barcha foydalanuvchilarga yuborish."""
    try:
        async with async_session() as session:
            tip = await db.get_random_tip(session)
            if not tip:
                logger.info("Kunlik maslahat topilmadi")
                return

            tip_text = texts.DAILY_TIP.format(tip=tip.tip_text)

            users = await db.get_all_users(session)
            success = 0
            for user in users:
                try:
                    await bot.send_message(user.telegram_id, tip_text, parse_mode="HTML")
                    success += 1
                except Exception:
                    pass

            logger.info(f"Kunlik maslahat {success} ta foydalanuvchiga yuborildi")
    except Exception as e:
        logger.error(f"Kunlik maslahat yuborishda xatolik: {e}")


def setup_scheduler(bot: Bot):
    """Schedulerni sozlash va ishga tushirish."""
    # Har kuni soat 9:00 da maslahat yuborish
    scheduler.add_job(
        send_daily_tip,
        "cron",
        hour=9,
        minute=0,
        args=[bot],
        id="daily_tip",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler ishga tushdi (kunlik maslahat: 09:00)")
