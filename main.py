import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import BOT_TOKEN, ADMIN_ID
from app.database.engine import create_db, async_session
from app.database.queries import seed_categories, seed_daily_tips
from app.middlewares.db import DbSessionMiddleware
from app.services.scheduler import setup_scheduler

# Handlers
from app.handlers import start, menu, resources, favorites, quiz, feedback
from app.handlers import admin_resources, admin_quiz, admin_broadcast, admin_stats, admin_feedback


async def on_startup(bot: Bot):
    """Bot ishga tushganda bajariladigan amallar."""
    logging.info("Bot ishga tushmoqda...")

    # Database yaratish
    await create_db()
    logging.info("Database tayyor")

    # Boshlang'ich ma'lumotlarni qo'shish
    async with async_session() as session:
        await seed_categories(session)
        await seed_daily_tips(session)
    logging.info("Seed data qo'shildi")

    # Scheduler ishga tushirish
    setup_scheduler(bot)

    # Adminga xabar
    try:
        await bot.send_message(
            ADMIN_ID,
            "🤖 <b>Kimyo Bot ishga tushdi!</b>\n\n"
            "⚙️ Admin panelga kirish uchun /admin buyrug'ini yuboring.",
            parse_mode="HTML",
        )
    except Exception as e:
        logging.warning(f"Adminga xabar yuborib bo'lmadi: {e}")

    logging.info("Bot tayyor!")


async def on_shutdown(bot: Bot):
    """Bot to'xtaganda bajariladigan amallar."""
    logging.info("Bot to'xtatilmoqda...")
    try:
        await bot.send_message(
            ADMIN_ID,
            "⚠️ <b>Kimyo Bot to'xtatildi.</b>",
            parse_mode="HTML",
        )
    except Exception:
        pass
    logging.info("Bot to'xtatildi.")


async def main():
    """Asosiy funksiya."""
    # Logging sozlash
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    # Token tekshirish
    if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
        logging.error("BOT_TOKEN .env faylida sozlanmagan!")
        sys.exit(1)

    if not ADMIN_ID or ADMIN_ID == 0:
        logging.error("ADMIN_ID .env faylida sozlanmagan!")
        sys.exit(1)

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware
    dp.update.middleware(DbSessionMiddleware())

    # Router'larni ulash — tartib muhim!
    # Admin router'lar avval (IsAdmin filtri bor)
    dp.include_router(admin_resources.router)
    dp.include_router(admin_quiz.router)
    dp.include_router(admin_broadcast.router)
    dp.include_router(admin_stats.router)
    dp.include_router(admin_feedback.router)

    # User router'lar
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(resources.router)
    dp.include_router(favorites.router)
    dp.include_router(quiz.router)
    dp.include_router(feedback.router)

    # Startup / Shutdown
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Polling boshlash
    logging.info("Polling boshlanmoqda...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi (Ctrl+C)")
