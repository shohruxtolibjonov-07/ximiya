from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import ADMIN_ID
from app.database import queries as db
from app.filters.admin import IsAdmin
from app.keyboards.inline import (
    admin_resource_list_kb, categories_kb, confirm_delete_kb
)
from app.keyboards.reply import admin_menu_kb, cancel_kb, skip_kb
from app.states.resource import AddCategoryState, AddResourceState, EditResourceState, AddingTipState
from app.utils import texts

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


# ========== KATEGORIYA QO'SHISH ==========

@router.message(F.text == "➕ Kategoriya qo'shish")
async def add_category_start(message: Message, state: FSMContext):
    await message.answer(texts.ADMIN_ENTER_CAT_NAME, reply_markup=cancel_kb())
    await state.set_state(AddCategoryState.waiting_name)


@router.message(AddCategoryState.waiting_name, F.text == "❌ Bekor qilish")
async def cancel_add_category(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(AddCategoryState.waiting_name)
async def process_cat_name(message: Message, state: FSMContext):
    await state.update_data(cat_name=message.text.strip())
    await message.answer(texts.ADMIN_ENTER_CAT_EMOJI, reply_markup=cancel_kb())
    await state.set_state(AddCategoryState.waiting_emoji)


@router.message(AddCategoryState.waiting_emoji, F.text == "❌ Bekor qilish")
async def cancel_add_category_emoji(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(AddCategoryState.waiting_emoji)
async def process_cat_emoji(message: Message, state: FSMContext, session: AsyncSession):
    emoji = message.text.strip()
    data = await state.get_data()
    await db.add_category(session, data["cat_name"], emoji)
    await message.answer(
        texts.ADMIN_CATEGORY_ADDED.format(emoji=emoji, name=data["cat_name"]),
        reply_markup=admin_menu_kb(),
    )
    await state.clear()


# ========== RESURS QO'SHISH ==========

@router.message(F.text == "📂 Resurs qo'shish")
async def add_resource_start(message: Message, state: FSMContext, session: AsyncSession):
    categories = await db.get_all_categories(session)
    if not categories:
        await message.answer("⚠️ Avval kategoriya qo'shing!")
        return

    await message.answer(
        texts.ADMIN_SELECT_CATEGORY,
        reply_markup=categories_kb(categories, prefix="addres_cat"),
    )
    await state.set_state(AddResourceState.waiting_category)


@router.callback_query(AddResourceState.waiting_category, F.data.startswith("addres_cat:"))
async def process_resource_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split(":")[1])
    await state.update_data(category_id=category_id)
    await callback.message.edit_text(texts.ADMIN_ENTER_TITLE)
    await state.set_state(AddResourceState.waiting_title)
    await callback.answer()


@router.message(AddResourceState.waiting_title, F.text == "❌ Bekor qilish")
async def cancel_add_resource_title(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(AddResourceState.waiting_title)
async def process_resource_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await message.answer(texts.ADMIN_ENTER_DESCRIPTION, reply_markup=skip_kb())
    await state.set_state(AddResourceState.waiting_description)


@router.message(AddResourceState.waiting_description, F.text == "❌ Bekor qilish")
async def cancel_add_resource_desc(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(AddResourceState.waiting_description)
async def process_resource_description(message: Message, state: FSMContext):
    desc = "" if message.text.strip() == "⏭ O'tkazib yuborish" else message.text.strip()
    await state.update_data(description=desc)
    await message.answer(texts.ADMIN_SEND_FILE, reply_markup=cancel_kb())
    await state.set_state(AddResourceState.waiting_file)


@router.message(AddResourceState.waiting_file, F.text == "❌ Bekor qilish")
async def cancel_add_resource_file(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(AddResourceState.waiting_file)
async def process_resource_file(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    data = await state.get_data()
    file_id = None
    file_type = "document"
    url = None

    if message.document:
        file_id = message.document.file_id
        file_type = "document"
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = "photo"
    elif message.video:
        file_id = message.video.file_id
        file_type = "video"
    elif message.text and ("http://" in message.text or "https://" in message.text):
        url = message.text.strip()
        file_type = "link"
    else:
        await message.answer("⚠️ Iltimos, fayl, rasm, video yoki havola yuboring.")
        return

    resource = await db.add_resource(
        session,
        title=data["title"],
        description=data.get("description", ""),
        category_id=data["category_id"],
        file_id=file_id,
        file_type=file_type,
        url=url,
    )

    await message.answer(
        texts.ADMIN_RESOURCE_ADDED.format(title=data["title"]),
        reply_markup=admin_menu_kb(),
    )
    await state.clear()

    # Barcha foydalanuvchilarga xabar
    users = await db.get_all_users(session)
    for user in users:
        if user.telegram_id != ADMIN_ID:
            try:
                await bot.send_message(
                    user.telegram_id,
                    f"📢 <b>Yangi resurs qo'shildi!</b>\n\n📄 {data['title']}",
                    parse_mode="HTML",
                )
            except Exception:
                pass


# ========== RESURSLAR RO'YXATI (ADMIN) ==========

@router.message(F.text == "📋 Resurslar ro'yxati")
async def admin_resources_list(message: Message, session: AsyncSession):
    resources = await db.get_all_resources_for_admin(session)
    if not resources:
        await message.answer(texts.ADMIN_NO_RESOURCES)
        return

    await message.answer(
        "📋 <b>Barcha resurslar:</b>",
        reply_markup=admin_resource_list_kb(resources),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("ares:"))
async def admin_resource_detail(callback: CallbackQuery, session: AsyncSession):
    resource_id = int(callback.data.split(":")[1])
    resource = await db.get_resource(session, resource_id)
    if not resource:
        await callback.answer("Resurs topilmadi!", show_alert=True)
        return

    category = await db.get_category(session, resource.category_id)
    pin_text = "📌 Qo'zg'almas" if resource.is_pinned else ""
    desc = resource.description or "Tavsif yo\u2018q"
    text = (
        f"📄 <b>{resource.title}</b>\n\n"
        f"📝 {desc}\n"
        f"📂 {category.name if category else '?'}\n"
        f"📅 {resource.created_at.strftime('%d.%m.%Y') if resource.created_at else ''}\n"
        f"{pin_text}"
    )

    from app.keyboards.inline import resource_detail_kb
    await callback.message.edit_text(
        text,
        reply_markup=resource_detail_kb(resource_id, is_admin=True),
        parse_mode="HTML",
    )
    await callback.answer()


# ========== TAHRIRLASH ==========

@router.callback_query(F.data.startswith("edit_res:"))
async def edit_resource_start(callback: CallbackQuery, state: FSMContext):
    resource_id = int(callback.data.split(":")[1])
    await state.update_data(edit_resource_id=resource_id)
    await callback.message.edit_text(texts.ADMIN_ENTER_NEW_DESC)
    await state.set_state(EditResourceState.waiting_new_description)
    await callback.answer()


@router.message(EditResourceState.waiting_new_description, F.text == "❌ Bekor qilish")
async def cancel_edit_resource(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(EditResourceState.waiting_new_description)
async def process_edit_resource(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    resource_id = data.get("edit_resource_id")
    await db.update_resource_description(session, resource_id, message.text.strip())
    await message.answer(texts.ADMIN_RESOURCE_UPDATED, reply_markup=admin_menu_kb())
    await state.clear()


# ========== PIN/UNPIN ==========

@router.callback_query(F.data.startswith("pin_res:"))
async def pin_resource(callback: CallbackQuery, session: AsyncSession):
    resource_id = int(callback.data.split(":")[1])
    is_pinned = await db.toggle_pin_resource(session, resource_id)
    if is_pinned:
        await callback.answer(texts.ADMIN_RESOURCE_PINNED, show_alert=True)
    else:
        await callback.answer(texts.ADMIN_RESOURCE_UNPINNED, show_alert=True)


# ========== O'CHIRISH ==========

@router.callback_query(F.data.startswith("del_res:"))
async def delete_resource_confirm(callback: CallbackQuery):
    resource_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        "🗑 Bu resursni o'chirishni tasdiqlaysizmi?",
        reply_markup=confirm_delete_kb("res", resource_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_del:res:"))
async def delete_resource_confirmed(callback: CallbackQuery, session: AsyncSession):
    resource_id = int(callback.data.split(":")[2])
    await db.delete_resource(session, resource_id)
    await callback.message.edit_text(texts.ADMIN_RESOURCE_DELETED)
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_del:"))
async def cancel_delete(callback: CallbackQuery):
    await callback.message.edit_text("❌ O'chirish bekor qilindi.")
    await callback.answer()


# ========== MASLAHAT QO'SHISH ==========

@router.message(F.text == "💡 Maslahat qo'shish")
async def add_tip_start(message: Message, state: FSMContext):
    await message.answer(texts.ADMIN_ENTER_TIP, reply_markup=cancel_kb())
    await state.set_state(AddingTipState.waiting_tip_text)


@router.message(AddingTipState.waiting_tip_text, F.text == "❌ Bekor qilish")
async def cancel_add_tip(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(AddingTipState.waiting_tip_text)
async def process_tip_text(message: Message, state: FSMContext, session: AsyncSession):
    await db.add_daily_tip(session, message.text.strip())
    await message.answer(texts.ADMIN_TIP_ADDED, reply_markup=admin_menu_kb())
    await state.clear()
