from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def main_menu_kb(is_admin: bool = False) -> ReplyKeyboardMarkup:
    """Asosiy menyu tugmalari."""
    keyboard = [
        [KeyboardButton(text="📚 Resurslar"), KeyboardButton(text="🔍 Qidirish")],
        [KeyboardButton(text="📝 Testlar"), KeyboardButton(text="⭐ Sevimlilar")],
        [KeyboardButton(text="🏆 Reyting"), KeyboardButton(text="📊 Mening natijalarim")],
        [KeyboardButton(text="💬 Fikr bildirish"), KeyboardButton(text="💡 Kunlik maslahat")],
    ]
    if is_admin:
        keyboard.append([KeyboardButton(text="⚙️ Admin panel")])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Bo'limni tanlang...",
    )


def admin_menu_kb() -> ReplyKeyboardMarkup:
    """Admin panel tugmalari."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📂 Resurs qo'shish"), KeyboardButton(text="📋 Resurslar ro'yxati")],
            [KeyboardButton(text="📝 Test yaratish"), KeyboardButton(text="📝 Testlar ro'yxati")],
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📢 Xabar yuborish")],
            [KeyboardButton(text="💬 Fikrlar"), KeyboardButton(text="➕ Kategoriya qo'shish")],
            [KeyboardButton(text="💡 Maslahat qo'shish"), KeyboardButton(text="🔙 Asosiy menyu")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Admin panel...",
    )


def cancel_kb() -> ReplyKeyboardMarkup:
    """Bekor qilish tugmasi."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True,
    )


def skip_kb() -> ReplyKeyboardMarkup:
    """O'tkazib yuborish tugmasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏭ O'tkazib yuborish")],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True,
    )


def confirm_kb() -> ReplyKeyboardMarkup:
    """Tasdiqlash tugmalari."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Ha"), KeyboardButton(text="❌ Yo'q")],
        ],
        resize_keyboard=True,
    )


remove_kb = ReplyKeyboardRemove()
