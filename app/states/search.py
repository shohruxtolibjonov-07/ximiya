from aiogram.fsm.state import State, StatesGroup


class SearchState(StatesGroup):
    waiting_keyword = State()
