from aiogram.fsm.state import State, StatesGroup


class CreateQuizState(StatesGroup):
    waiting_title = State()
    waiting_category = State()
    waiting_question_text = State()
    waiting_option_a = State()
    waiting_option_b = State()
    waiting_option_c = State()
    waiting_option_d = State()
    waiting_correct = State()
    waiting_more = State()


class TakeQuizState(StatesGroup):
    answering = State()
