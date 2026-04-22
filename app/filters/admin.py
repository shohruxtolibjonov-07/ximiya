from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from app.config import ADMIN_ID


class IsAdmin(BaseFilter):
    """Faqat admin uchun ruxsat beruvchi filtr."""

    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        return event.from_user.id == ADMIN_ID
