from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_contact_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Поделитесь Контактом", request_contact=True)
    builder.button(text="🔙 Назад")
    builder.adjust(1, 1)
    return builder.as_markup(resize_keyboard=True)
