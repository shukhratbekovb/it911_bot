from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_start_kb(lang="ru"):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Уже клиент")
    builder.button(text="Стать клиентом")
    builder.button(text="О Нас")
    # builder.button(text="Выбрать Язык")

    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)


def get_lang_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="", callback_data="lang_ru")
    builder.button(text="", callback_data="lang_en")
    builder.button(text="", callback_data="lang_uz")
    builder.adjust(3)

    return builder.as_markup()
def get_back_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔙 Назад")
    return builder.as_markup(resize_keyboard=True)
