import asyncio

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.database import queries as db
from app.keyboards.reply import admin_menu_kb, cancel_kb, confirm_kb
from app.states.broadcast import BroadcastState
from app.utils import texts

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(F.text == "📢 Xabar yuborish")
async def broadcast_start(message: Message, state: FSMContext):
    await message.answer(texts.ADMIN_BROADCAST_PROMPT, reply_markup=cancel_kb())
    await state.set_state(BroadcastState.waiting_content)


@router.message(BroadcastState.waiting_content, F.text == "❌ Bekor qilish")
async def cancel_broadcast(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(BroadcastState.waiting_content)
async def process_broadcast_content(message: Message, state: FSMContext, session: AsyncSession):
    """Broadcast xabar kontentini qabul qilish."""
    users = await db.get_all_users(session)
    count = len(users)

    await state.update_data(
        broadcast_msg_id=message.message_id,
        broadcast_chat_id=message.chat.id,
        users_count=count,
    )

    # Xabar turini aniqlash va saqlash
    if message.text:
        await state.update_data(msg_type="text", msg_text=message.text)
    elif message.photo:
        await state.update_data(
            msg_type="photo",
            file_id=message.photo[-1].file_id,
            msg_text=message.caption or "",
        )
    elif message.video:
        await state.update_data(
            msg_type="video",
            file_id=message.video.file_id,
            msg_text=message.caption or "",
        )
    elif message.document:
        await state.update_data(
            msg_type="document",
            file_id=message.document.file_id,
            msg_text=message.caption or "",
        )
    else:
        await message.answer("⚠️ Bu turdagi xabar qo'llab-quvvatlanmaydi.")
        return

    await message.answer(
        texts.ADMIN_BROADCAST_CONFIRM.format(count=count),
        reply_markup=confirm_kb(),
    )
    await state.set_state(BroadcastState.waiting_confirm)


@router.message(BroadcastState.waiting_confirm, F.text == "❌ Yo'q")
async def cancel_broadcast_confirm(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(BroadcastState.waiting_confirm, F.text == "✅ Ha")
async def confirm_broadcast(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    """Broadcast xabarni yuborish."""
    data = await state.get_data()
    users = await db.get_all_users(session)

    success = 0
    total = len(users)

    await message.answer("📢 Xabar yuborilmoqda...")

    for user in users:
        try:
            msg_type = data.get("msg_type", "text")
            if msg_type == "text":
                await bot.send_message(user.telegram_id, data["msg_text"])
            elif msg_type == "photo":
                await bot.send_photo(
                    user.telegram_id,
                    data["file_id"],
                    caption=data.get("msg_text", ""),
                )
            elif msg_type == "video":
                await bot.send_video(
                    user.telegram_id,
                    data["file_id"],
                    caption=data.get("msg_text", ""),
                )
            elif msg_type == "document":
                await bot.send_document(
                    user.telegram_id,
                    data["file_id"],
                    caption=data.get("msg_text", ""),
                )
            success += 1
            await asyncio.sleep(0.05)  # Anti-flood
        except Exception:
            pass

    await message.answer(
        texts.ADMIN_BROADCAST_DONE.format(success=success, total=total),
        reply_markup=admin_menu_kb(),
    )
    await state.clear()
