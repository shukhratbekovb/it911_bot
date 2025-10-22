from aiogram.fsm.state import StatesGroup, State


class AuthForm(StatesGroup):
    lang = State()
