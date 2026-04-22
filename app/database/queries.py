from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import (
    Category, DailyTip, Favorite, Feedback, Question,
    Quiz, QuizResult, Resource, User
)


# ==================== USERS ====================

async def add_user(session: AsyncSession, telegram_id: int, full_name: str) -> User:
    user = User(telegram_id=telegram_id, full_name=full_name)
    session.add(user)
    await session.commit()
    return user


async def get_user(session: AsyncSession, telegram_id: int) -> Optional[User]:
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def update_user_center(session: AsyncSession, telegram_id: int, center: str):
    await session.execute(
        update(User).where(User.telegram_id == telegram_id).values(learning_center=center)
    )
    await session.commit()


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User).where(User.is_active == True))
    return result.scalars().all()


async def get_users_by_center(session: AsyncSession, center: str) -> Sequence[User]:
    result = await session.execute(
        select(User).where(User.learning_center == center, User.is_active == True)
    )
    return result.scalars().all()


async def get_user_count(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(User.id)))
    return result.scalar() or 0


async def get_user_count_by_center(session: AsyncSession, center: str) -> int:
    result = await session.execute(
        select(func.count(User.id)).where(User.learning_center == center)
    )
    return result.scalar() or 0


async def get_all_users_for_export(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


# ==================== CATEGORIES ====================

async def add_category(session: AsyncSession, name: str, emoji: str = "📁") -> Category:
    cat = Category(name=name, emoji=emoji)
    session.add(cat)
    await session.commit()
    return cat


async def get_all_categories(session: AsyncSession) -> Sequence[Category]:
    result = await session.execute(select(Category))
    return result.scalars().all()


async def get_category(session: AsyncSession, category_id: int) -> Optional[Category]:
    result = await session.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def delete_category(session: AsyncSession, category_id: int):
    await session.execute(delete(Category).where(Category.id == category_id))
    await session.commit()


# ==================== RESOURCES ====================

async def add_resource(
    session: AsyncSession,
    title: str,
    description: str,
    category_id: int,
    file_id: str = None,
    file_type: str = "document",
    url: str = None,
) -> Resource:
    resource = Resource(
        title=title,
        description=description,
        category_id=category_id,
        file_id=file_id,
        file_type=file_type,
        url=url,
    )
    session.add(resource)
    await session.commit()
    return resource


async def get_resources_by_category(
    session: AsyncSession, category_id: int, offset: int = 0, limit: int = 5
) -> Sequence[Resource]:
    result = await session.execute(
        select(Resource)
        .where(Resource.category_id == category_id)
        .order_by(Resource.is_pinned.desc(), Resource.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def get_resource_count_by_category(session: AsyncSession, category_id: int) -> int:
    result = await session.execute(
        select(func.count(Resource.id)).where(Resource.category_id == category_id)
    )
    return result.scalar() or 0


async def get_resource(session: AsyncSession, resource_id: int) -> Optional[Resource]:
    result = await session.execute(
        select(Resource).where(Resource.id == resource_id)
    )
    return result.scalar_one_or_none()


async def delete_resource(session: AsyncSession, resource_id: int):
    await session.execute(delete(Favorite).where(Favorite.resource_id == resource_id))
    await session.execute(delete(Resource).where(Resource.id == resource_id))
    await session.commit()


async def update_resource_description(session: AsyncSession, resource_id: int, new_desc: str):
    await session.execute(
        update(Resource).where(Resource.id == resource_id).values(description=new_desc)
    )
    await session.commit()


async def toggle_pin_resource(session: AsyncSession, resource_id: int) -> bool:
    resource = await get_resource(session, resource_id)
    if resource:
        new_val = not resource.is_pinned
        await session.execute(
            update(Resource).where(Resource.id == resource_id).values(is_pinned=new_val)
        )
        await session.commit()
        return new_val
    return False


async def search_resources(session: AsyncSession, keyword: str) -> Sequence[Resource]:
    result = await session.execute(
        select(Resource)
        .where(
            (Resource.title.ilike(f"%{keyword}%"))
            | (Resource.description.ilike(f"%{keyword}%"))
        )
        .order_by(Resource.is_pinned.desc(), Resource.created_at.desc())
        .limit(20)
    )
    return result.scalars().all()


async def get_all_resources(session: AsyncSession) -> Sequence[Resource]:
    result = await session.execute(
        select(Resource).order_by(Resource.is_pinned.desc(), Resource.created_at.desc())
    )
    return result.scalars().all()


async def get_all_resources_for_admin(session: AsyncSession) -> Sequence[Resource]:
    result = await session.execute(
        select(Resource)
        .options(selectinload(Resource.category))
        .order_by(Resource.created_at.desc())
    )
    return result.scalars().all()


# ==================== FAVORITES ====================

async def add_favorite(session: AsyncSession, user_id: int, resource_id: int) -> Favorite:
    fav = Favorite(user_id=user_id, resource_id=resource_id)
    session.add(fav)
    await session.commit()
    return fav


async def remove_favorite(session: AsyncSession, user_id: int, resource_id: int):
    await session.execute(
        delete(Favorite).where(
            Favorite.user_id == user_id, Favorite.resource_id == resource_id
        )
    )
    await session.commit()


async def get_favorites(session: AsyncSession, user_id: int) -> Sequence[Favorite]:
    result = await session.execute(
        select(Favorite)
        .options(selectinload(Favorite.resource))
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
    )
    return result.scalars().all()


async def is_favorite(session: AsyncSession, user_id: int, resource_id: int) -> bool:
    result = await session.execute(
        select(Favorite).where(
            Favorite.user_id == user_id, Favorite.resource_id == resource_id
        )
    )
    return result.scalar_one_or_none() is not None


# ==================== QUIZZES ====================

async def add_quiz(session: AsyncSession, title: str, category: str = None) -> Quiz:
    quiz = Quiz(title=title, category=category)
    session.add(quiz)
    await session.commit()
    return quiz


async def add_question(
    session: AsyncSession,
    quiz_id: int,
    text: str,
    option_a: str,
    option_b: str,
    option_c: str,
    option_d: str,
    correct_option: str,
    order_num: int = 0,
) -> Question:
    q = Question(
        quiz_id=quiz_id,
        text=text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_option=correct_option.upper(),
        order_num=order_num,
    )
    session.add(q)
    await session.commit()
    return q


async def get_active_quizzes(session: AsyncSession) -> Sequence[Quiz]:
    result = await session.execute(
        select(Quiz).where(Quiz.is_active == True).order_by(Quiz.created_at.desc())
    )
    return result.scalars().all()


async def get_all_quizzes(session: AsyncSession) -> Sequence[Quiz]:
    result = await session.execute(select(Quiz).order_by(Quiz.created_at.desc()))
    return result.scalars().all()


async def get_quiz(session: AsyncSession, quiz_id: int) -> Optional[Quiz]:
    result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
    return result.scalar_one_or_none()


async def get_questions(session: AsyncSession, quiz_id: int) -> Sequence[Question]:
    result = await session.execute(
        select(Question)
        .where(Question.quiz_id == quiz_id)
        .order_by(Question.order_num)
    )
    return result.scalars().all()


async def toggle_quiz_active(session: AsyncSession, quiz_id: int) -> bool:
    quiz = await get_quiz(session, quiz_id)
    if quiz:
        new_val = not quiz.is_active
        await session.execute(
            update(Quiz).where(Quiz.id == quiz_id).values(is_active=new_val)
        )
        await session.commit()
        return new_val
    return False


async def delete_quiz(session: AsyncSession, quiz_id: int):
    await session.execute(delete(QuizResult).where(QuizResult.quiz_id == quiz_id))
    await session.execute(delete(Question).where(Question.quiz_id == quiz_id))
    await session.execute(delete(Quiz).where(Quiz.id == quiz_id))
    await session.commit()


async def get_random_quiz(session: AsyncSession) -> Optional[Quiz]:
    result = await session.execute(
        select(Quiz).where(Quiz.is_active == True).order_by(func.random()).limit(1)
    )
    return result.scalar_one_or_none()


# ==================== QUIZ RESULTS ====================

async def save_quiz_result(
    session: AsyncSession, user_id: int, quiz_id: int, score: int, total: int
) -> QuizResult:
    qr = QuizResult(user_id=user_id, quiz_id=quiz_id, score=score, total=total)
    session.add(qr)
    await session.commit()
    return qr


async def get_user_quiz_results(session: AsyncSession, user_id: int) -> Sequence[QuizResult]:
    result = await session.execute(
        select(QuizResult)
        .options(selectinload(QuizResult.quiz))
        .where(QuizResult.user_id == user_id)
        .order_by(QuizResult.completed_at.desc())
    )
    return result.scalars().all()


async def get_leaderboard(session: AsyncSession, limit: int = 10):
    """Eng yaxshi natijalar bo'yicha reytingni qaytaradi."""
    result = await session.execute(
        select(
            QuizResult.user_id,
            User.full_name,
            func.sum(QuizResult.score).label("total_score"),
            func.sum(QuizResult.total).label("total_questions"),
            func.count(QuizResult.id).label("tests_taken"),
        )
        .join(User, User.telegram_id == QuizResult.user_id)
        .group_by(QuizResult.user_id, User.full_name)
        .order_by(func.sum(QuizResult.score).desc())
        .limit(limit)
    )
    return result.all()


async def get_user_progress(session: AsyncSession, user_id: int):
    """Foydalanuvchining umumiy progressini qaytaradi."""
    result = await session.execute(
        select(
            func.count(QuizResult.id).label("tests_taken"),
            func.sum(QuizResult.score).label("total_score"),
            func.sum(QuizResult.total).label("total_questions"),
        )
        .where(QuizResult.user_id == user_id)
    )
    row = result.one_or_none()
    if row and row.tests_taken:
        return {
            "tests_taken": row.tests_taken,
            "total_score": row.total_score or 0,
            "total_questions": row.total_questions or 0,
            "percentage": round((row.total_score / row.total_questions) * 100, 1) if row.total_questions else 0,
        }
    return {"tests_taken": 0, "total_score": 0, "total_questions": 0, "percentage": 0}


# ==================== FEEDBACK ====================

async def add_feedback(session: AsyncSession, user_id: int, message: str) -> Feedback:
    fb = Feedback(user_id=user_id, message=message)
    session.add(fb)
    await session.commit()
    return fb


async def get_all_feedback(session: AsyncSession, unread_only: bool = False) -> Sequence[Feedback]:
    query = select(Feedback).options(selectinload(Feedback.user))
    if unread_only:
        query = query.where(Feedback.is_read == False)
    query = query.order_by(Feedback.created_at.desc())
    result = await session.execute(query)
    return result.scalars().all()


async def mark_feedback_read(session: AsyncSession, feedback_id: int):
    await session.execute(
        update(Feedback).where(Feedback.id == feedback_id).values(is_read=True)
    )
    await session.commit()


async def get_unread_feedback_count(session: AsyncSession) -> int:
    result = await session.execute(
        select(func.count(Feedback.id)).where(Feedback.is_read == False)
    )
    return result.scalar() or 0


# ==================== DAILY TIPS ====================

async def add_daily_tip(session: AsyncSession, tip_text: str) -> DailyTip:
    tip = DailyTip(tip_text=tip_text)
    session.add(tip)
    await session.commit()
    return tip


async def get_random_tip(session: AsyncSession) -> Optional[DailyTip]:
    result = await session.execute(
        select(DailyTip).where(DailyTip.is_used == False).order_by(func.random()).limit(1)
    )
    tip = result.scalar_one_or_none()
    if tip is None:
        # Barcha maslahatlar ishlatilgan — qayta boshlash
        await session.execute(update(DailyTip).values(is_used=False))
        await session.commit()
        result = await session.execute(
            select(DailyTip).order_by(func.random()).limit(1)
        )
        tip = result.scalar_one_or_none()
    if tip:
        await session.execute(
            update(DailyTip).where(DailyTip.id == tip.id).values(is_used=True)
        )
        await session.commit()
    return tip


# ==================== SEED DATA ====================

async def seed_categories(session: AsyncSession):
    """Boshlang'ich kategoriyalarni qo'shish."""
    cats = [
        ("Organik kimyo", "🧪"),
        ("Anorganik kimyo", "⚗️"),
        ("Umumiy kimyo", "📐"),
        ("Testlar", "📝"),
        ("Video darslar", "🎬"),
        ("Darsliklar", "📖"),
    ]
    for name, emoji in cats:
        existing = await session.execute(
            select(Category).where(Category.name == name)
        )
        if not existing.scalar_one_or_none():
            session.add(Category(name=name, emoji=emoji))
    await session.commit()


async def seed_daily_tips(session: AsyncSession):
    """Boshlang'ich kimyo maslahatlarini qo'shish."""
    tips = [
        "💡 Bilasizmi? Suv (H₂O) — er yuzidagi eng ko'p tarqalgan moddadir.",
        "💡 Olmos va grafit bir xil element — ugleroddan tashkil topgan, lekin tuzilishi farq qiladi.",
        "💡 Kimyoviy elementlarning 75% dan ortig'i metallardir.",
        "💡 Vodorod — koinotdagi eng ko'p tarqalgan elementdir.",
        "💡 Geliy Quyoshda kashf etilgan — shuning uchun yunon tilida 'helios' (quyosh) deb atalgan.",
        "💡 Oltin — kimyoviy jihatdan eng barqaror metallardan biri, u deyarli hech qanday kislota bilan reaksiyaga kirishmaydi.",
        "💡 Davriy jadval birinchi marta 1869-yilda Dmitriy Mendeleyev tomonidan nashr etilgan.",
        "💡 Ftorli kislota (HF) shishani eritishi mumkin.",
        "💡 Inert gazlar (18-guruh) o'ta barqaror, ular deyarli hech qanday reaksiyaga kirishmaydi.",
        "💡 Fosfor qorong'ida porlaydi — shuning uchun uning nomi yunon tilida 'yorug'lik olib keluvchi' degan ma'noni anglatadi.",
        "💡 Natriy va kaliy metallari suvda portlab reaksiyaga kirishadi.",
        "💡 Kislorod atmosferaning 21% ni tashkil qiladi.",
        "💡 Kimyoviy bog'lanishning 3 turi bor: kovalent, ion va metall bog'lanish.",
        "💡 Oltingugurt vulqonlar yaqinida tabiiy holda topiladi.",
        "💡 pH shkala 0 dan 14 gacha bo'lib, 7 — neytral muhit.",
    ]
    existing = await session.execute(select(func.count(DailyTip.id)))
    count = existing.scalar() or 0
    if count == 0:
        for tip_text in tips:
            session.add(DailyTip(tip_text=tip_text))
        await session.commit()
