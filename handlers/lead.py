from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.lead import get_contact_kb
from keyboards.start import get_start_kb, get_back_kb
from services.api import ApiService
from states.lead import LeadForm

router = Router()
EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PHONE_PATTERN = r"^\+?\d{9,15}$"


@router.message(F.text == "🔙 Назад", LeadForm.email)
async def back_from_email(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:", reply_markup=None)
    await state.set_state(LeadForm.full_name)


@router.message(F.text == "🔙 Назад", LeadForm.phone)
async def back_from_phone(message: Message, state: FSMContext):
    await message.answer("Введите вашу почту:", reply_markup=get_back_kb())
    await state.set_state(LeadForm.email)


@router.message(F.text == "🔙 Назад", LeadForm.company_name)
async def back_from_company_name(message: Message, state: FSMContext):
    await message.answer("Введите номер телефона:", reply_markup=get_back_kb())
    await state.set_state(LeadForm.phone)


@router.message(F.text == "🔙 Назад", LeadForm.company_info)
async def back_from_company_info(message: Message, state: FSMContext):
    await message.answer("Введите название компании:", reply_markup=get_back_kb())
    await state.set_state(LeadForm.company_name)


@router.message(F.text, LeadForm.full_name)
async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer("Введите свою почту:", reply_markup=get_back_kb())
    await state.set_state(LeadForm.email)


@router.message(~F.text, LeadForm.full_name)
async def get_wrong_full_name(message: Message, state: FSMContext):
    await message.answer("Вы ввели неправильно попробуйте еще раз")
    await state.set_state(LeadForm.full_name)


@router.message(F.text.regexp(EMAIL_PATTERN), LeadForm.email)
async def get_email(message: Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Поделитесь своим номером телефона: ", reply_markup=get_contact_kb())
    await state.set_state(LeadForm.phone)


@router.message(~F.text | ~F.text.regexp(EMAIL_PATTERN), LeadForm.email)
async def wrong_email(message: Message, state: FSMContext):
    await message.answer(
        "❌ Пожалуйста, введите корректный e-mail текстом (пример: `example@gmail.com`)."
    )
    await state.set_state(LeadForm.email)


@router.message(F.text.regexp(PHONE_PATTERN) | F.contact, LeadForm.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text.strip() if not message.contact else message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer("✅ Телефон сохранён.\nВведите название компании:", reply_markup=get_back_kb())
    await state.set_state(LeadForm.company_name)


# --- Ошибка: не текст или неверный формат ---
@router.message(~F.text | ~F.text.regexp(PHONE_PATTERN), LeadForm.phone)
async def wrong_phone(message: Message, state: FSMContext):
    await message.answer(
        "❌ Введите корректный номер телефона в формате:\n"
        "`+998901234567` или `901234567`.",
        reply_markup=get_back_kb(),
    )


@router.message(F.text, LeadForm.company_name)
async def get_company_name(message: Message, state: FSMContext):
    company_name = message.text.strip()
    await state.update_data(company_name=company_name)
    await message.answer("Введите информацию о компании:", reply_markup=get_back_kb())
    await state.set_state(LeadForm.company_info)


# --- Не текст (фото, видео и т.д.) ---
@router.message(~F.text, LeadForm.company_name)
async def wrong_company_name(message: Message, state: FSMContext):
    await message.answer(
        "❌ Пожалуйста, введите название компании текстом, а не отправляйте файл или картинку.",
        reply_markup=get_back_kb(),
    )
@router.message(F.text, LeadForm.company_info)
async def get_company_info(message: Message, state: FSMContext):
    company_info = message.text.strip()

    # Можно добавить простую проверку на минимальную длину
    if len(company_info) < 10:
        await message.answer(
            "❌ Опишите компанию чуть подробнее (минимум 10 символов).",
            reply_markup=get_back_kb(),
        )
        return

    await state.update_data(company_info=company_info)

    data = await state.get_data()
    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")
    company_name = data.get("company_name")
    target_id = data.get("target_id")

    service = ApiService()
    response = service.create_lead(
        data={
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "company_name": company_name,
            "company_info": company_info,
            "target_id": target_id,
        },
        target_id=target_id
    )
    if not response:
        await message.answer("Временно не работает", reply_markup=get_start_kb())


    await message.answer(
        "✅ Отлично! Ваша анкета заполнена:\n\n"
        f"👤 Имя: {full_name}\n"
        f"📧 Почта: {email}\n"
        f"📱 Телефон: {phone}\n"
        f"🏢 Компания: {company_name}\n"
        f"ℹ️ О компании: {company_info}\n\n"
        "Спасибо за регистрацию!",
        reply_markup=get_start_kb(),
    )

    await state.clear()

# --- Не текст (фото, видео, документ и т.п.) ---
@router.message(~F.text, LeadForm.company_info)
async def wrong_company_info(message: Message, state: FSMContext):
    await message.answer(
        "❌ Пожалуйста, введите информацию о компании текстом, без изображений и файлов.",
        reply_markup=get_back_kb(),
    )