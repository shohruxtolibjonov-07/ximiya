from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import queries as db
from app.keyboards.inline import quiz_list_kb, quiz_options_kb
from app.keyboards.reply import main_menu_kb
from app.states.quiz import TakeQuizState
from app.utils import texts

router = Router()


@router.message(F.text == "📝 Testlar")
async def show_quizzes(message: Message, session: AsyncSession):
    """Faol testlar ro'yxatini ko'rsatish."""
    quizzes = await db.get_active_quizzes(session)
    if not quizzes:
        await message.answer(texts.NO_QUIZZES)
        return

    await message.answer(
        texts.QUIZZES_TITLE,
        reply_markup=quiz_list_kb(quizzes),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("quiz:"))
async def start_quiz(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Testni boshlash."""
    quiz_id = int(callback.data.split(":")[1])
    quiz = await db.get_quiz(session, quiz_id)
    if not quiz:
        await callback.answer("Test topilmadi!", show_alert=True)
        return

    questions = await db.get_questions(session, quiz_id)
    if not questions:
        await callback.answer("Bu testda savollar yo'q!", show_alert=True)
        return

    # FSM da test ma'lumotlarini saqlash
    questions_data = []
    for q in questions:
        questions_data.append({
            "id": q.id,
            "text": q.text,
            "a": q.option_a,
            "b": q.option_b,
            "c": q.option_c,
            "d": q.option_d,
            "correct": q.correct_option,
        })

    await state.set_data({
        "quiz_id": quiz_id,
        "quiz_title": quiz.title,
        "questions": questions_data,
        "current": 0,
        "score": 0,
        "total": len(questions_data),
    })

    # Birinchi savolni ko'rsatish
    await _show_question(callback.message, state, edit=True)
    await state.set_state(TakeQuizState.answering)
    await callback.answer()


@router.callback_query(F.data == "random_quiz")
async def start_random_quiz(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Tasodifiy testni boshlash."""
    quiz = await db.get_random_quiz(session)
    if not quiz:
        await callback.answer(texts.NO_RANDOM_QUIZ, show_alert=True)
        return

    questions = await db.get_questions(session, quiz.id)
    if not questions:
        await callback.answer("Bu testda savollar yo'q!", show_alert=True)
        return

    questions_data = []
    for q in questions:
        questions_data.append({
            "id": q.id,
            "text": q.text,
            "a": q.option_a,
            "b": q.option_b,
            "c": q.option_c,
            "d": q.option_d,
            "correct": q.correct_option,
        })

    await state.set_data({
        "quiz_id": quiz.id,
        "quiz_title": quiz.title,
        "questions": questions_data,
        "current": 0,
        "score": 0,
        "total": len(questions_data),
    })

    await _show_question(callback.message, state, edit=True)
    await state.set_state(TakeQuizState.answering)
    await callback.answer()


@router.callback_query(TakeQuizState.answering, F.data.startswith("ans:"))
async def process_answer(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Javobni qayta ishlash."""
    parts = callback.data.split(":")
    answer = parts[2].upper()

    data = await state.get_data()
    current = data["current"]
    questions = data["questions"]
    question = questions[current]

    # Javobni tekshirish
    is_correct = answer == question["correct"]
    if is_correct:
        data["score"] += 1
        result_text = texts.QUIZ_CORRECT
    else:
        result_text = texts.QUIZ_WRONG.format(correct=question["correct"])

    await callback.answer(result_text, show_alert=True)

    # Keyingi savolga o'tish
    data["current"] += 1
    await state.set_data(data)

    if data["current"] < data["total"]:
        # Keyingi savol
        await _show_question(callback.message, state, edit=True)
    else:
        # Test yakunlandi
        score = data["score"]
        total = data["total"]
        percentage = round((score / total) * 100, 1) if total > 0 else 0
        emoji, comment = texts.get_quiz_comment(percentage)

        # Natijani saqlash
        await db.save_quiz_result(session, callback.from_user.id, data["quiz_id"], score, total)

        await callback.message.edit_text(
            texts.QUIZ_RESULT.format(
                title=data["quiz_title"],
                score=score,
                total=total,
                percentage=percentage,
                emoji=emoji,
                comment=comment,
            ),
            parse_mode="HTML",
        )
        await state.clear()


async def _show_question(message, state: FSMContext, edit: bool = False):
    """Joriy savolni ko'rsatish."""
    data = await state.get_data()
    current = data["current"]
    question = data["questions"][current]

    text = texts.QUIZ_QUESTION.format(
        current=current + 1,
        total=data["total"],
        text=question["text"],
        a=question["a"],
        b=question["b"],
        c=question["c"],
        d=question["d"],
    )

    kb = quiz_options_kb(current)

    if edit:
        await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    else:
        await message.answer(text, reply_markup=kb, parse_mode="HTML")
