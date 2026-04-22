from typing import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.models import Category, Quiz, Resource


def center_selection_kb() -> InlineKeyboardMarkup:
    """O'quv markaz tanlash tugmalari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏫 Akademiya", callback_data="center:Akademiya")],
            [InlineKeyboardButton(text="🏫 Ilm-nur", callback_data="center:Ilm-nur")],
        ]
    )


def categories_kb(categories: Sequence[Category], prefix: str = "cat") -> InlineKeyboardMarkup:
    """Kategoriyalar ro'yxati tugmalari."""
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(
            text=f"{cat.emoji} {cat.name}",
            callback_data=f"{prefix}:{cat.id}"
        )
    builder.adjust(2)
    return builder.as_markup()


def resources_list_kb(
    resources: Sequence[Resource],
    category_id: int,
    offset: int,
    total: int,
    page_size: int = 5,
    is_admin: bool = False,
) -> InlineKeyboardMarkup:
    """Resurslar ro'yxati + pagination."""
    builder = InlineKeyboardBuilder()

    for res in resources:
        pin = "📌 " if res.is_pinned else ""
        builder.button(
            text=f"{pin}{res.title}",
            callback_data=f"res:{res.id}"
        )

    builder.adjust(1)

    # Pagination tugmalari
    nav_buttons = []
    if offset > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="◀️ Oldingi",
                callback_data=f"page:{category_id}:{offset - page_size}"
            )
        )
    if offset + page_size < total:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Keyingi ▶️",
                callback_data=f"page:{category_id}:{offset + page_size}"
            )
        )
    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(InlineKeyboardButton(text="🔙 Kategoriyalar", callback_data="back_to_cats"))

    return builder.as_markup()


def resource_detail_kb(resource_id: int, is_fav: bool = False, is_admin: bool = False) -> InlineKeyboardMarkup:
    """Resurs tafsilotlari tugmalari."""
    builder = InlineKeyboardBuilder()

    fav_text = "💔 Sevimlilardan o'chirish" if is_fav else "⭐ Sevimlilarga qo'shish"
    builder.button(text=fav_text, callback_data=f"fav:{resource_id}")

    if is_admin:
        builder.button(text="✏️ Tahrirlash", callback_data=f"edit_res:{resource_id}")
        builder.button(text="📌 Pin", callback_data=f"pin_res:{resource_id}")
        builder.button(text="🗑 O'chirish", callback_data=f"del_res:{resource_id}")

    builder.button(text="🔙 Orqaga", callback_data=f"back_to_res_list:{resource_id}")
    builder.adjust(1)
    return builder.as_markup()


def favorites_kb(favorites) -> InlineKeyboardMarkup:
    """Sevimlilar ro'yxati."""
    builder = InlineKeyboardBuilder()
    for fav in favorites:
        if fav.resource:
            builder.button(
                text=f"⭐ {fav.resource.title}",
                callback_data=f"res:{fav.resource_id}"
            )
    builder.adjust(1)
    return builder.as_markup()


def quiz_list_kb(quizzes: Sequence[Quiz]) -> InlineKeyboardMarkup:
    """Testlar ro'yxati."""
    builder = InlineKeyboardBuilder()
    for quiz in quizzes:
        builder.button(
            text=f"📝 {quiz.title}",
            callback_data=f"quiz:{quiz.id}"
        )
    builder.button(text="🎲 Tasodifiy test", callback_data="random_quiz")
    builder.adjust(1)
    return builder.as_markup()


def quiz_options_kb(question_index: int) -> InlineKeyboardMarkup:
    """Savol variantlari (A/B/C/D)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🅰️ A", callback_data=f"ans:{question_index}:A"),
                InlineKeyboardButton(text="🅱️ B", callback_data=f"ans:{question_index}:B"),
            ],
            [
                InlineKeyboardButton(text="🅲 C", callback_data=f"ans:{question_index}:C"),
                InlineKeyboardButton(text="🅳 D", callback_data=f"ans:{question_index}:D"),
            ],
        ]
    )


def admin_quiz_list_kb(quizzes: Sequence[Quiz]) -> InlineKeyboardMarkup:
    """Admin uchun testlar ro'yxati."""
    builder = InlineKeyboardBuilder()
    for quiz in quizzes:
        status = "✅" if quiz.is_active else "❌"
        builder.button(
            text=f"{status} {quiz.title}",
            callback_data=f"aquiz:{quiz.id}"
        )
    builder.adjust(1)
    return builder.as_markup()


def admin_quiz_actions_kb(quiz_id: int, is_active: bool) -> InlineKeyboardMarkup:
    """Admin uchun test amallari."""
    toggle_text = "❌ Nofaol qilish" if is_active else "✅ Faollashtirish"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=toggle_text, callback_data=f"toggle_quiz:{quiz_id}")],
            [InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"del_quiz:{quiz_id}")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_quiz_list")],
        ]
    )


def admin_resource_list_kb(resources: Sequence[Resource]) -> InlineKeyboardMarkup:
    """Admin uchun resurslar ro'yxati."""
    builder = InlineKeyboardBuilder()
    for res in resources:
        pin = "📌 " if res.is_pinned else ""
        cat_name = res.category.name if res.category else "?"
        builder.button(
            text=f"{pin}{res.title} [{cat_name}]",
            callback_data=f"ares:{res.id}"
        )
    builder.adjust(1)
    return builder.as_markup()


def confirm_delete_kb(item_type: str, item_id: int) -> InlineKeyboardMarkup:
    """O'chirishni tasdiqlash."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"confirm_del:{item_type}:{item_id}"),
                InlineKeyboardButton(text="❌ Yo'q", callback_data=f"cancel_del:{item_type}"),
            ]
        ]
    )


def search_results_kb(resources: Sequence[Resource]) -> InlineKeyboardMarkup:
    """Qidiruv natijalari."""
    builder = InlineKeyboardBuilder()
    for res in resources:
        builder.button(
            text=f"📄 {res.title}",
            callback_data=f"res:{res.id}"
        )
    builder.adjust(1)
    return builder.as_markup()


def stats_export_kb() -> InlineKeyboardMarkup:
    """Statistika eksport tugmalari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📥 CSV eksport", callback_data="export:csv")],
            [InlineKeyboardButton(text="📥 Excel eksport", callback_data="export:xlsx")],
        ]
    )
