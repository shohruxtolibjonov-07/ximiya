from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import ADMIN_ID
from app.database import queries as db
from app.keyboards.inline import (
    categories_kb, resource_detail_kb, resources_list_kb, search_results_kb
)
from app.states.search import SearchState
from app.utils import texts

router = Router()


@router.message(F.text == "📚 Resurslar")
async def show_categories(message: Message, session: AsyncSession):
    """Kategoriyalar ro'yxatini ko'rsatish."""
    categories = await db.get_all_categories(session)
    if not categories:
        await message.answer("📭 Hali kategoriyalar yo'q.")
        return

    await message.answer(
        texts.CATEGORIES_TITLE,
        reply_markup=categories_kb(categories),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("cat:"))
async def show_resources_by_category(callback: CallbackQuery, session: AsyncSession):
    """Kategoriya bo'yicha resurslarni ko'rsatish."""
    category_id = int(callback.data.split(":")[1])
    await _show_resources_page(callback, session, category_id, 0)
    await callback.answer()


@router.callback_query(F.data.startswith("page:"))
async def paginate_resources(callback: CallbackQuery, session: AsyncSession):
    """Resurslar sahifasini almashtirish."""
    parts = callback.data.split(":")
    category_id = int(parts[1])
    offset = int(parts[2])
    await _show_resources_page(callback, session, category_id, offset)
    await callback.answer()


async def _show_resources_page(
    callback: CallbackQuery, session: AsyncSession, category_id: int, offset: int
):
    """Resurslar sahifasini ko'rsatish (ichki funksiya)."""
    page_size = 5
    resources = await db.get_resources_by_category(session, category_id, offset, page_size)
    total = await db.get_resource_count_by_category(session, category_id)
    category = await db.get_category(session, category_id)

    if not resources:
        await callback.message.edit_text(texts.NO_RESOURCES)
        return

    cat_name = category.name if category else "Noma'lum"
    total_pages = max(1, (total - 1) // page_size + 1)
    current_page = offset // page_size + 1
    text = f"📂 <b>{cat_name}</b> — {total} ta resurs\n\nSahifa: {current_page}/{total_pages}"

    is_admin = callback.from_user.id == ADMIN_ID
    await callback.message.edit_text(
        text,
        reply_markup=resources_list_kb(resources, category_id, offset, total, page_size, is_admin),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("res:"))
async def show_resource_detail(callback: CallbackQuery, session: AsyncSession):
    """Resurs tafsilotlarini ko'rsatish."""
    resource_id = int(callback.data.split(":")[1])
    resource = await db.get_resource(session, resource_id)

    if not resource:
        await callback.answer("Resurs topilmadi!", show_alert=True)
        return

    category = await db.get_category(session, resource.category_id)
    is_fav = await db.is_favorite(session, callback.from_user.id, resource_id)
    is_admin = callback.from_user.id == ADMIN_ID

    pinned = texts.RESOURCE_PINNED if resource.is_pinned else ""
    text = texts.RESOURCE_DETAIL.format(
        title=resource.title,
        description=resource.description or "Tavsif yo'q",
        category=category.name if category else "Noma'lum",
        date=resource.created_at.strftime("%d.%m.%Y") if resource.created_at else "",
        pinned=pinned,
    )

    # Faylni (yoki havolani) yuborish
    try:
        if resource.file_id:
            if resource.file_type == "photo":
                await callback.message.answer_photo(
                    resource.file_id,
                    caption=text,
                    reply_markup=resource_detail_kb(resource_id, is_fav, is_admin),
                    parse_mode="HTML",
                )
            elif resource.file_type == "video":
                await callback.message.answer_video(
                    resource.file_id,
                    caption=text,
                    reply_markup=resource_detail_kb(resource_id, is_fav, is_admin),
                    parse_mode="HTML",
                )
            else:
                await callback.message.answer_document(
                    resource.file_id,
                    caption=text,
                    reply_markup=resource_detail_kb(resource_id, is_fav, is_admin),
                    parse_mode="HTML",
                )
        elif resource.url:
            text += f"\n\n🔗 <a href='{resource.url}'>Havolani ochish</a>"
            await callback.message.edit_text(
                text,
                reply_markup=resource_detail_kb(resource_id, is_fav, is_admin),
                parse_mode="HTML",
                disable_web_page_preview=False,
            )
        else:
            await callback.message.edit_text(
                text,
                reply_markup=resource_detail_kb(resource_id, is_fav, is_admin),
                parse_mode="HTML",
            )
    except Exception:
        await callback.message.edit_text(
            text,
            reply_markup=resource_detail_kb(resource_id, is_fav, is_admin),
            parse_mode="HTML",
        )

    await callback.answer()


@router.callback_query(F.data == "back_to_cats")
async def back_to_categories(callback: CallbackQuery, session: AsyncSession):
    """Kategoriyalar ro'yxatiga qaytish."""
    categories = await db.get_all_categories(session)
    await callback.message.edit_text(
        texts.CATEGORIES_TITLE,
        reply_markup=categories_kb(categories),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("back_to_res_list:"))
async def back_to_resource_list(callback: CallbackQuery, session: AsyncSession):
    """Resurslar ro'yxatiga qaytish."""
    resource_id = int(callback.data.split(":")[1])
    resource = await db.get_resource(session, resource_id)
    if resource:
        await _show_resources_page(callback, session, resource.category_id, 0)
    await callback.answer()


# ========== SEARCH ==========

@router.message(F.text == "🔍 Qidirish")
async def search_prompt(message: Message, state: FSMContext):
    """Qidirish rejimini boshlash."""
    await message.answer(texts.SEARCH_PROMPT)
    await state.set_state(SearchState.waiting_keyword)


@router.message(SearchState.waiting_keyword, F.text == "❌ Bekor qilish")
async def cancel_search(message: Message, state: FSMContext):
    """Qidiruvni bekor qilish."""
    from app.keyboards.reply import main_menu_kb
    await state.clear()
    await message.answer(
        texts.CANCELLED,
        reply_markup=main_menu_kb(is_admin=message.from_user.id == ADMIN_ID),
    )


@router.message(SearchState.waiting_keyword)
async def search_handler(message: Message, state: FSMContext, session: AsyncSession):
    """Qidirish natijalarini ko'rsatish."""
    if not message.text:
        await message.answer("⚠️ Iltimos, matn kiriting.")
        return

    keyword = message.text.strip()
    if len(keyword) < 2:
        await message.answer("⚠️ Kamida 2 belgi kiriting.")
        return

    resources = await db.search_resources(session, keyword)
    if not resources:
        await message.answer(
            texts.SEARCH_NO_RESULTS.format(keyword=keyword),
        )
        return

    await message.answer(
        texts.SEARCH_RESULTS.format(keyword=keyword, count=len(resources)),
        reply_markup=search_results_kb(resources),
        parse_mode="HTML",
    )
    await state.clear()
