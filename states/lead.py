from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    full_name = State()
    email = State()
    phone = State()
    company_name = State()
    company_info = State()
    target_id = State()
