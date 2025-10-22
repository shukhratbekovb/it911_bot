from aiogram import Router, F
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.start import get_start_kb
from states.lead import LeadForm

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    args = message.text.split()
    if len(args) == 1:
        await message.answer("Добро Пожаловать", reply_markup=get_start_kb())
        await state.clear()
    else:
        target_id = args[1]
        await message.answer("🎯 Добро пожаловать! Похоже, вы пришли по рекламе.\n\nВведите ваше ФИО:")
        await state.set_state(LeadForm.full_name)
        await state.update_data(target_id=target_id)


@router.message(F.text == "О Нас")
async def about_handler(message: Message):
    await message.answer(
"""💡 **О компании IT 911**  
        
Мы создаём **IT-решения**, которые делают бизнес проще.  
Наш сервис объединяет **CRM**, **учёт**, **поддержку**, **автоматизацию** и **аналитику** — всё в одном подписочном пакете.  
        
📦 **Что мы предлагаем:**
• **CRM-системы** — продажи, клиенты, напоминания  
• **Учёт и аналитика** — финансы, склад, отчёты  
• **Поддержка 24/7** — быстро реагируем и решаем проблемы  
• **Автоматизация** — Telegram-боты, интеграции с сайтами и 1С  
• **Техническое сопровождение** — хостинг, резервное копирование, безопасность  
        
🎯 **Наша цель:**
Помочь компаниям любого масштаба **расти**, не тратя время и ресурсы на поиск десятков подрядчиков.  
Мы объединяем всё, что нужно для **стабильной цифровой работы бизнеса** — в одном месте.  
        
⚙️ **Наши преимущества:**
• **Минимальные затраты (TCO)**  
• **Искусственный интеллект** и автоматизация процессов  
• **Гибкая система подписок и тарифов**  
• **Локализация** под рынок Узбекистана  
• **Экономия** за счёт объединения 5–6 сервисов  
        
🌐 **Подробнее на нашем сайте:**  
👉 https://it911.uz
        
📞 **Контакты:**  
✉️ info@it911.com  
📱 +998 90 329 77 00  
📍 **Chorsu MFY, дом 4, кв. 135**"""
    )


@router.message(F.text == "Стать Клиентом")
async def lead_handler(message: Message, state: FSMContext):
    await message.answer("Введите ваше ФИО:")
    await state.set_state(LeadForm.full_name)


@router.message(F.text == "Уже Клиент")
async def company_handler(message: Message):
    await message.answer("В Этапе Разработки")
