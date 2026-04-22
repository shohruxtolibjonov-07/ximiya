from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.database import queries as db
from app.keyboards.inline import admin_quiz_actions_kb, admin_quiz_list_kb
from app.keyboards.reply import admin_menu_kb, cancel_kb, confirm_kb
from app.states.quiz import CreateQuizState
from app.utils import texts

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(F.text == "📝 Test yaratish")
async def create_quiz_start(message: Message, state: FSMContext):
    await message.answer(texts.ADMIN_ENTER_QUIZ_TITLE, reply_markup=cancel_kb())
    await state.set_state(CreateQuizState.waiting_title)


@router.message(CreateQuizState.waiting_title, F.text == "❌ Bekor qilish")
async def cancel_create_quiz(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(CreateQuizState.waiting_title)
async def process_quiz_title(message: Message, state: FSMContext):
    await state.update_data(quiz_title=message.text.strip())
    await message.answer(texts.ADMIN_ENTER_QUIZ_CAT, reply_markup=cancel_kb())
    await state.set_state(CreateQuizState.waiting_category)


@router.message(CreateQuizState.waiting_category, F.text == "❌ Bekor qilish")
async def cancel_quiz_category(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(CreateQuizState.waiting_category)
async def process_quiz_category(message: Message, state: FSMContext, session: AsyncSession):
    quiz_title = (await state.get_data())["quiz_title"]
    quiz = await db.add_quiz(session, quiz_title, message.text.strip())
    await state.update_data(
        quiz_id=quiz.id,
        question_num=1,
        questions_count=0,
    )
    await message.answer(
        texts.ADMIN_ENTER_QUESTION.format(num=1),
        reply_markup=cancel_kb(),
    )
    await state.set_state(CreateQuizState.waiting_question_text)


@router.message(CreateQuizState.waiting_question_text, F.text == "❌ Bekor qilish")
async def cancel_quiz_question(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=admin_menu_kb())


@router.message(CreateQuizState.waiting_question_text)
async def process_question_text(message: Message, state: FSMContext):
    await state.update_data(q_text=message.text.strip())
    await message.answer(texts.ADMIN_ENTER_OPTION_A)
    await state.set_state(CreateQuizState.waiting_option_a)


@router.message(CreateQuizState.waiting_option_a)
async def process_option_a(message: Message, state: FSMContext):
    await state.update_data(opt_a=message.text.strip())
    await message.answer(texts.ADMIN_ENTER_OPTION_B)
    await state.set_state(CreateQuizState.waiting_option_b)


@router.message(CreateQuizState.waiting_option_b)
async def process_option_b(message: Message, state: FSMContext):
    await state.update_data(opt_b=message.text.strip())
    await message.answer(texts.ADMIN_ENTER_OPTION_C)
    await state.set_state(CreateQuizState.waiting_option_c)


@router.message(CreateQuizState.waiting_option_c)
async def process_option_c(message: Message, state: FSMContext):
    await state.update_data(opt_c=message.text.strip())
    await message.answer(texts.ADMIN_ENTER_OPTION_D)
    await state.set_state(CreateQuizState.waiting_option_d)


@router.message(CreateQuizState.waiting_option_d)
async def process_option_d(message: Message, state: FSMContext):
    await state.update_data(opt_d=message.text.strip())
    await message.answer(texts.ADMIN_ENTER_CORRECT)
    await state.set_state(CreateQuizState.waiting_correct)


@router.message(CreateQuizState.waiting_correct)
async def process_correct_answer(message: Message, state: FSMContext, session: AsyncSession):
    answer = message.text.strip().upper()
    if answer not in ("A", "B", "C", "D"):
        await message.answer("⚠️ Iltimos, A, B, C yoki D kiriting:")
        return

    data = await state.get_data()
    await db.add_question(
        session,
        quiz_id=data["quiz_id"],
        text=data["q_text"],
        option_a=data["opt_a"],
        option_b=data["opt_b"],
        option_c=data["opt_c"],
        option_d=data["opt_d"],
        correct_option=answer,
        order_num=data["question_num"],
    )

    new_count = data["questions_count"] + 1
    await state.update_data(questions_count=new_count, question_num=data["question_num"] + 1)

    await message.answer(
        texts.ADMIN_QUESTION_ADDED.format(num=data["question_num"]),
        reply_markup=confirm_kb(),
    )
    await state.set_state(CreateQuizState.waiting_more)


@router.message(CreateQuizState.waiting_more, F.text == "✅ Ha")
async def add_more_questions(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        texts.ADMIN_ENTER_QUESTION.format(num=data["question_num"]),
        reply_markup=cancel_kb(),
    )
    await state.set_state(CreateQuizState.waiting_question_text)


@router.message(CreateQuizState.waiting_more, F.text == "❌ Yo'q")
async def finish_quiz_creation(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        texts.ADMIN_QUIZ_CREATED.format(
            title=data["quiz_title"],
            count=data["questions_count"],
        ),
        reply_markup=admin_menu_kb(),
    )
    await state.clear()


# ========== TESTLAR RO'YXATI (ADMIN) ==========

@router.message(F.text == "📝 Testlar ro'yxati")
async def admin_quizzes_list(message: Message, session: AsyncSession):
    quizzes = await db.get_all_quizzes(session)
    if not quizzes:
        await message.answer(texts.NO_QUIZZES)
        return

    await message.answer(
        "📝 <b>Barcha testlar:</b>",
        reply_markup=admin_quiz_list_kb(quizzes),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("aquiz:"))
async def admin_quiz_detail(callback: CallbackQuery, session: AsyncSession):
    quiz_id = int(callback.data.split(":")[1])
    quiz = await db.get_quiz(session, quiz_id)
    if not quiz:
        await callback.answer("Test topilmadi!", show_alert=True)
        return

    questions = await db.get_questions(session, quiz_id)
    text = (
        f"📝 <b>{quiz.title}</b>\n\n"
        f"📂 Kategoriya: {quiz.category or 'Umumiy'}\n"
        f"❓ Savollar soni: {len(questions)}\n"
        f"{'✅ Faol' if quiz.is_active else '❌ Nofaol'}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=admin_quiz_actions_kb(quiz_id, quiz.is_active),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("toggle_quiz:"))
async def toggle_quiz(callback: CallbackQuery, session: AsyncSession):
    quiz_id = int(callback.data.split(":")[1])
    is_active = await db.toggle_quiz_active(session, quiz_id)
    if is_active:
        await callback.answer(texts.ADMIN_QUIZ_TOGGLED_ON, show_alert=True)
    else:
        await callback.answer(texts.ADMIN_QUIZ_TOGGLED_OFF, show_alert=True)

    # Yangilash
    quiz = await db.get_quiz(session, quiz_id)
    questions = await db.get_questions(session, quiz_id)
    text = (
        f"📝 <b>{quiz.title}</b>\n\n"
        f"📂 Kategoriya: {quiz.category or 'Umumiy'}\n"
        f"❓ Savollar soni: {len(questions)}\n"
        f"{'✅ Faol' if quiz.is_active else '❌ Nofaol'}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=admin_quiz_actions_kb(quiz_id, quiz.is_active),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("del_quiz:"))
async def delete_quiz_confirm(callback: CallbackQuery):
    quiz_id = int(callback.data.split(":")[1])
    from app.keyboards.inline import confirm_delete_kb
    await callback.message.edit_text(
        "🗑 Bu testni o'chirishni tasdiqlaysizmi?",
        reply_markup=confirm_delete_kb("quiz", quiz_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_del:quiz:"))
async def delete_quiz_confirmed(callback: CallbackQuery, session: AsyncSession):
    quiz_id = int(callback.data.split(":")[2])
    await db.delete_quiz(session, quiz_id)
    await callback.message.edit_text(texts.ADMIN_QUIZ_DELETED)
    await callback.answer()


@router.callback_query(F.data == "back_to_quiz_list")
async def back_to_quiz_list(callback: CallbackQuery, session: AsyncSession):
    quizzes = await db.get_all_quizzes(session)
    if not quizzes:
        await callback.message.edit_text(texts.NO_QUIZZES)
    else:
        await callback.message.edit_text(
            "📝 <b>Barcha testlar:</b>",
            reply_markup=admin_quiz_list_kb(quizzes),
            parse_mode="HTML",
        )
    await callback.answer()
