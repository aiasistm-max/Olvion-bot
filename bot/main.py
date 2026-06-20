        import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

class AgentState(StatesGroup):
    jorlan_task = State()
    cfo_task = State()
    smm_task = State()

def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Создать задачу")],
            [KeyboardButton(text="🤖 Мои агенты")],
            [KeyboardButton(text="📊 Проекты (CRM)")],
            [KeyboardButton(text="🔍 Сканер сообщений")],
            [KeyboardButton(text="⏱️ Активные задачи")],
            [KeyboardButton(text="⚙️ Настройки")],
        ],
        resize_keyboard=True
    )

def get_agents_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎯 Джорлин (лендинги)", callback_data="agent_jorlan")],
            [InlineKeyboardButton(text="💰 CFO-Консультант", callback_data="agent_cfo")],
            [InlineKeyboardButton(text="📱 SMM Admin", callback_data="agent_smm")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
        ]
    )
    return keyboard

async def main():
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")        return
    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        welcome = f"👋 Добро пожаловать, {message.from_user.full_name}!\n\n🤖 Я - Профессор Олвион\nВаш интеллектуальный помощник\n\n🎯 Что я умею:\n• Создавать и управлять задачами\n• Оркестрировать ИИ-агентов\n• Сканировать сообщения\n• Вести CRM\n\n💡 Нажмите на кнопку внизу, чтобы начать!"
        await message.answer(welcome, reply_markup=get_main_menu())
    
    @dp.message()
    async def handle_buttons(message: Message, state: FSMContext):
        await state.clear()
        text = message.text
        
        if text == "📝 Создать задачу":
            await message.answer("📝 Создание задачи\n\nОпишите вашу задачу:", reply_markup=get_agents_menu())
        
        elif text == "🤖 Мои агенты":
            agents_text = "🤖 Ваши ИИ-агенты:\n\n"
            agents_text += "🎯 <b>Джорлин</b>\n"
            agents_text += "Архитектор лендингов и веб-приложений\n"
            agents_text += "Создает структуру, дизайн, тексты\n\n"
            agents_text += "💰 <b>CFO-Консультант</b>\n"
            agents_text += "Финансовый анализ и планирование\n"
            agents_text += "ROI, бюджеты, прогнозы\n\n"
            agents_text += "📱 <b>SMM Admin</b>\n"
            agents_text += "Управление социальными сетями\n"
            agents_text += "Контент-план, посты, аналитика\n\n"
            await message.answer(agents_text, reply_markup=get_agents_menu())
        
        elif text == "📊 Проекты (CRM)":
            await message.answer("📊 Ваши проекты\n\nПока нет проектов. Создайте первую задачу!")
        
        elif text == "🔍 Сканер сообщений":
            await message.answer("🔍 Сканер личных сообщений\n\nАгент читает чаты и присылает сводку:\n• кто ждет ответа\n• где деньги\n• где срочное\n\nФункция в разработке...")
        
        elif text == "⏱️ Активные задачи":
            await message.answer("⏱️ Активные задачи\n\nНет активных задач")
        
        elif text == "⚙️ Настройки":
            await message.answer(f"⚙️ Настройки\n\nВаш ID: {message.from_user.id}\nUsername: @{message.from_user.username or 'не указан'}")

    @dp.callback_query()
    async def handle_agent_callback(callback: InlineKeyboardButton, state: FSMContext):
        data = callback.data
        
        if data == "main_menu":
            await callback.message.edit_text("Главное меню", reply_markup=get_main_menu())
                elif data == "agent_jorlan":
            await state.set_state(AgentState.jorlan_task)
            await callback.message.answer(
                "🎯 <b>Джорлин активирован!</b>\n\n"
                "Опишите ваш проект лендинга:\n"
                "• Какой продукт/услуга?\n"
                "• Целевая аудитория?\n"
                "• Основные блоки?\n"
                "• Пожелания по дизайну?\n\n"
                "Или нажмите /cancel для отмены"
            )
        
        elif data == "agent_cfo":
            await state.set_state(AgentState.cfo_task)
            await callback.message.answer(
                "💰 <b>CFO-Консультант активирован!</b>\n\n"
                "Опишите вашу финансовую задачу:\n"
                "• Расчет бюджета?\n"
                "• Анализ ROI?\n"
                "• Финансовое планирование?\n"
                "• Другое?\n\n"
                "Или нажмите /cancel для отмены"
            )
        
        elif data == "agent_smm":
            await state.set_state(AgentState.smm_task)
            await callback.message.answer(
                "📱 <b>SMM Admin активирован!</b>\n\n"
                "Опишите вашу SMM задачу:\n"
                "• Контент-план?\n"
                "• Создание постов?\n"
                "• Аналитика?\n"
                "• Стратегия продвижения?\n\n"
                "Или нажмите /cancel для отмены"
            )
        
        await callback.answer()

    @dp.message(AgentState.jorlan_task)
    async def jorlan_handler(message: Message, state: FSMContext):
        task = message.text
        response = f"🎯 <b>Джорлин получил задачу!</b>\n\n📝 <b>Задача:</b> {task}\n\n⏳ <b>Статус:</b> В работе...\n\n🔜 <i>Скоро будет интеграция с AI для генерации лендинга!</i>\n\nАгент проанализирует:\n• Целевую аудиторию\n• Структуру лендинга\n• Контент и тексты\n• Дизайн и UX\n\n✅ Результат будет готов soon!"
        await message.answer(response)
        await state.clear()

    @dp.message(AgentState.cfo_task)
    async def cfo_handler(message: Message, state: FSMContext):
        task = message.text
        response = f"💰 <b>CFO получил задачу!</b>\n\n📝 <b>Задача:</b> {task}\n\n⏳ <b>Статус:</b> В работе...\n\n🔜 <i>Скоро будет интеграция с AI для финансового анализа!</i>\n\nАгент проанализирует:\n• Бюджет проекта\n• ROI и окупаемость\n• Финансовые риски\n• Прогнозы\n\n✅ Результат будет готов soon!"
        await message.answer(response)        await state.clear()

    @dp.message(AgentState.smm_task)
    async def smm_handler(message: Message, state: FSMContext):
        task = message.text
        response = f"📱 <b>SMM Admin получил задачу!</b>\n\n📝 <b>Задача:</b> {task}\n\n⏳ <b>Статус:</b> В работе...\n\n🔜 <i>Скоро будет интеграция с AI для SMM!</i>\n\nАгент создаст:\n• Контент-план\n• Посты для соцсетей\n• Хэштеги\n• Аналитику\n\n✅ Результат будет готов soon!"
        await message.answer(response)
        await state.clear()

    @dp.message(Command("cancel"))
    async def cancel_handler(message: Message, state: FSMContext):
        await state.clear()
        await message.answer("❌ Отменено. Выберите действие:", reply_markup=get_main_menu())

    logger.info("🚀 Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
