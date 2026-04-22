from aiogram.fsm.state import State, StatesGroup


class BroadcastState(StatesGroup):
    waiting_content = State()
    waiting_confirm = State()
