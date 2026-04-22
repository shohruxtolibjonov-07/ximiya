"""Barcha o'zbek tilidagi matnlar."""

WELCOME = (
    "🧪 <b>Kimyo Bot</b>ga xush kelibsiz!\n\n"
    "Bu bot sizga kimyo fanidan resurslar, testlar va foydali materiallar bilan yordam beradi.\n\n"
    "📝 Ro'yxatdan o'tish uchun ism-familiyangizni kiriting:"
)

WELCOME_BACK = (
    "👋 Qaytib kelganingizdan xursandmiz, <b>{name}</b>!\n\n"
    "Quyidagi bo'limlardan birini tanlang:"
)

ASK_CENTER = (
    "🏫 Qaysi o'quv markazida o'qiysiz?\n\n"
    "Quyidagilardan birini tanlang:"
)

REGISTRATION_DONE = (
    "✅ <b>Ro'yxatdan muvaffaqiyatli o'tdingiz!</b>\n\n"
    "👤 Ism: <b>{name}</b>\n"
    "🏫 O'quv markaz: <b>{center}</b>\n\n"
    "Endi barcha bo'limlardan foydalanishingiz mumkin!"
)

MAIN_MENU = "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:"

ADMIN_MENU = (
    "⚙️ <b>Admin panel</b>\n\n"
    "Kerakli amalni tanlang:"
)

# ========== RESOURCES ==========

CATEGORIES_TITLE = "📂 <b>Kategoriyalar</b>\n\nKerakli kategoriyani tanlang:"

NO_RESOURCES = "📭 Bu kategoriyada hali resurs yo'q."

RESOURCE_DETAIL = (
    "📄 <b>{title}</b>\n\n"
    "📝 {description}\n\n"
    "📂 Kategoriya: {category}\n"
    "📅 Qo'shilgan: {date}\n"
    "{pinned}"
)

RESOURCE_PINNED = "📌 <i>Muhim material</i>"

# ========== SEARCH ==========

SEARCH_PROMPT = "🔍 Qidirish uchun kalit so'zni yozing:"

SEARCH_RESULTS = "🔍 <b>Qidiruv natijalari:</b> «{keyword}»\n\n{count} ta natija topildi:"

SEARCH_NO_RESULTS = "😔 «{keyword}» bo'yicha hech narsa topilmadi.\n\nBoshqa kalit so'z bilan urinib ko'ring."

# ========== FAVORITES ==========

FAVORITES_TITLE = "⭐ <b>Sevimli resurslaringiz:</b>"

NO_FAVORITES = "⭐ Sevimli resurslaringiz hali yo'q.\n\nResurs sahifasida ⭐ tugmasini bosib qo'shishingiz mumkin."

ADDED_TO_FAVORITES = "⭐ Sevimlilarga qo'shildi!"

REMOVED_FROM_FAVORITES = "💔 Sevimlilardan o'chirildi!"

# ========== QUIZZES ==========

QUIZZES_TITLE = "📝 <b>Mavjud testlar:</b>\n\nTestni tanlang yoki tasodifiy test boshlang:"

NO_QUIZZES = "📝 Hozircha testlar yo'q.\n\nTez orada yangi testlar qo'shiladi!"

QUIZ_START = (
    "📝 <b>{title}</b>\n\n"
    "📊 Savollar soni: {total}\n\n"
    "Tayyor bo'lsangiz, savollarga javob bering!"
)

QUIZ_QUESTION = (
    "❓ <b>Savol {current}/{total}</b>\n\n"
    "{text}\n\n"
    "🅰️ {a}\n"
    "🅱️ {b}\n"
    "🅲 {c}\n"
    "🅳 {d}"
)

QUIZ_CORRECT = "✅ To'g'ri!"
QUIZ_WRONG = "❌ Noto'g'ri! To'g'ri javob: {correct}"

QUIZ_RESULT = (
    "🏁 <b>Test yakunlandi!</b>\n\n"
    "📝 Test: <b>{title}</b>\n"
    "✅ To'g'ri javoblar: <b>{score}/{total}</b>\n"
    "📊 Natija: <b>{percentage}%</b>\n\n"
    "{emoji} {comment}"
)

NO_RANDOM_QUIZ = "🎲 Hozircha faol testlar yo'q."

# ========== LEADERBOARD ==========

LEADERBOARD_TITLE = "🏆 <b>Reyting jadvali</b>\n\n"

LEADERBOARD_ROW = "{rank}. {medal} <b>{name}</b> — {score}/{total} ({pct}%)\n"

LEADERBOARD_EMPTY = "🏆 Reyting hali bo'sh.\n\nTestlardan o'ting va reytingga kiring!"

# ========== PROGRESS ==========

USER_PROGRESS = (
    "📊 <b>Sizning natijalaringiz:</b>\n\n"
    "📝 O'tilgan testlar: <b>{tests}</b>\n"
    "✅ To'g'ri javoblar: <b>{score}/{total}</b>\n"
    "📊 Umumiy ball: <b>{pct}%</b>"
)

# ========== FEEDBACK ==========

FEEDBACK_PROMPT = "💬 Fikr yoki savolingizni yozing:\n\n(Bekor qilish uchun ❌ Bekor qilish tugmasini bosing)"

FEEDBACK_SENT = "✅ Fikringiz muvaffaqiyatli yuborildi!\n\nRahmat! Tez orada javob beramiz."

FEEDBACK_RECEIVED = (
    "💬 <b>Yangi fikr!</b>\n\n"
    "👤 {name} (ID: {user_id})\n"
    "🏫 {center}\n\n"
    "💬 {message}"
)

# ========== DAILY TIP ==========

DAILY_TIP = "🧪 <b>Kunlik kimyo maslahati:</b>\n\n{tip}"

NO_TIPS = "💡 Hozircha maslahatlar qo'shilmagan."

# ========== ADMIN ==========

ADMIN_ONLY = "⛔ Bu buyruq faqat admin uchun!"

# Admin - Resource
ADMIN_SELECT_CATEGORY = "📂 Resurs uchun kategoriyani tanlang:"
ADMIN_ENTER_TITLE = "📝 Resurs nomini kiriting:"
ADMIN_ENTER_DESCRIPTION = "📝 Resurs tavsifini kiriting:\n\n(O'tkazib yuborish uchun ⏭ tugmasini bosing)"
ADMIN_SEND_FILE = "📎 Faylni yuboring (PDF, DOCX, rasm, video) yoki havolani kiriting:"
ADMIN_RESOURCE_ADDED = "✅ Resurs muvaffaqiyatli qo'shildi!\n\n📄 {title}"
ADMIN_RESOURCE_DELETED = "🗑 Resurs o'chirildi!"
ADMIN_RESOURCE_UPDATED = "✏️ Resurs yangilandi!"
ADMIN_RESOURCE_PINNED = "📌 Resurs qo'zg'almas qilindi!"
ADMIN_RESOURCE_UNPINNED = "📌 Resurs qo'zg'almasdan olib tashlandi!"
ADMIN_ENTER_NEW_DESC = "✏️ Yangi tavsifni kiriting:"
ADMIN_NO_RESOURCES = "📭 Hali resurslar yo'q."

# Admin - Category
ADMIN_ENTER_CAT_NAME = "📂 Yangi kategoriya nomini kiriting:"
ADMIN_ENTER_CAT_EMOJI = "😀 Kategoriya uchun emoji kiriting (masalan: 🧪):"
ADMIN_CATEGORY_ADDED = "✅ Kategoriya qo'shildi: {emoji} {name}"

# Admin - Quiz
ADMIN_ENTER_QUIZ_TITLE = "📝 Test nomini kiriting:"
ADMIN_ENTER_QUIZ_CAT = "📂 Test kategoriyasini kiriting (masalan: Organik kimyo):"
ADMIN_ENTER_QUESTION = "❓ {num}-savol matnini kiriting:"
ADMIN_ENTER_OPTION_A = "🅰️ A variantni kiriting:"
ADMIN_ENTER_OPTION_B = "🅱️ B variantni kiriting:"
ADMIN_ENTER_OPTION_C = "🅲 C variantni kiriting:"
ADMIN_ENTER_OPTION_D = "🅳 D variantni kiriting:"
ADMIN_ENTER_CORRECT = "✅ To'g'ri javobni kiriting (A, B, C yoki D):"
ADMIN_QUESTION_ADDED = "✅ {num}-savol qo'shildi!\n\nYana savol qo'shasizmi?"
ADMIN_QUIZ_CREATED = "✅ Test muvaffaqiyatli yaratildi!\n\n📝 {title}\n❓ Savollar soni: {count}"
ADMIN_QUIZ_DELETED = "🗑 Test o'chirildi!"
ADMIN_QUIZ_TOGGLED_ON = "✅ Test faollashtirildi!"
ADMIN_QUIZ_TOGGLED_OFF = "❌ Test nofaol qilindi!"

# Admin - Broadcast
ADMIN_BROADCAST_PROMPT = "📢 Barcha foydalanuvchilarga yuboriladigan xabarni kiriting:\n\n(Matn, rasm, video yoki fayl yuboring)"
ADMIN_BROADCAST_CONFIRM = "📢 Xabar {count} ta foydalanuvchiga yuborilsinmi?"
ADMIN_BROADCAST_DONE = "✅ Xabar {success}/{total} ta foydalanuvchiga yuborildi!"

# Admin - Stats
ADMIN_STATS = (
    "📊 <b>Statistika</b>\n\n"
    "👥 Jami foydalanuvchilar: <b>{total}</b>\n"
    "🏫 Akademiya: <b>{akademiya}</b>\n"
    "🏫 Ilm-nur: <b>{ilmnur}</b>\n"
    "📚 Jami resurslar: <b>{resources}</b>\n"
    "📝 Jami testlar: <b>{quizzes}</b>\n"
    "💬 O'qilmagan fikrlar: <b>{feedbacks}</b>"
)

# Admin - Feedback
ADMIN_FEEDBACKS_TITLE = "💬 <b>Foydalanuvchi fikrlari:</b>\n\n"
ADMIN_NO_FEEDBACKS = "💬 Hozircha fikrlar yo'q."
ADMIN_FEEDBACK_ITEM = (
    "💬 #{id}\n"
    "👤 {name}\n"
    "🏫 {center}\n"
    "📅 {date}\n"
    "💬 {message}\n"
    "{'✅ O\'qilgan' if is_read else '🔴 Yangi'}\n"
    "───────────────\n"
)

# Admin - Daily tip
ADMIN_ENTER_TIP = "💡 Yangi kunlik maslahat matnini kiriting:"
ADMIN_TIP_ADDED = "✅ Maslahat qo'shildi!"

# ========== CANCEL ==========

CANCELLED = "❌ Bekor qilindi."

# ========== ERRORS ==========

ERROR = "⚠️ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
INVALID_INPUT = "⚠️ Noto'g'ri kiritish. Iltimos, qaytadan urinib ko'ring."


def get_quiz_comment(percentage: float) -> tuple:
    """Ball bo'yicha emoji va izoh qaytaradi."""
    if percentage >= 90:
        return "🌟", "Ajoyib natija! Siz kimyo ustasisiz!"
    elif percentage >= 70:
        return "👏", "Yaxshi natija! Ozgina harakat va mukammal bo'lasiz!"
    elif percentage >= 50:
        return "👍", "Yomon emas! Ko'proq mashq qiling!"
    else:
        return "💪", "Hafsala qilmang! Ko'proq o'qing va qaytadan urinib ko'ring!"
