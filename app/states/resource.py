from aiogram.fsm.state import State, StatesGroup


class AddResourceState(StatesGroup):
    waiting_category = State()
    waiting_title = State()
    waiting_description = State()
    waiting_file = State()


class EditResourceState(StatesGroup):
    waiting_resource_id = State()
    waiting_new_description = State()


class AddCategoryState(StatesGroup):
    waiting_name = State()
    waiting_emoji = State()


class AddingTipState(StatesGroup):
    waiting_tip_text = State()

