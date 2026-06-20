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

# Машина состояний для агентов
class AgentState(StatesGroup):
    jorlan_task = State()
    cfo_task = State()
    smm_task = State()

# Главное меню
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

# Меню выбора агента
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
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return
    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    # Команда /start
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        welcome = f"👋 Добро пожаловать, {message.from_user.full_name}!\n\n🤖 Я - Профессор Олвион\nВаш интеллектуальный помощник\n\n🎯 Что я умею:\n• Создавать и управлять задачами\n• Оркестрировать ИИ-агентов\n• Сканировать сообщения\n• Вести CRM\n\n💡 Нажмите на кнопку внизу, чтобы начать!"
        await message.answer(welcome, reply_markup=get_main_menu())
    
    # Обработчик кнопок главного меню
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

    # Обработчик callback (выбор агента)
    @dp.callback_query()    async def handle_agent_callback(callback: InlineKeyboardButton, state: FSMContext):
        data = callback.data
        
        if data == "main_menu":
            await callback.message.edit_text("Главное меню", reply_markup=get_main_menu())
        
        elif data == "agent_jorlan":
            await state.set_state(AgentState.jorlan_task)
            await callback.message.answer(
                "🎯 <b>Джорлин активирован!</b>\n\n"
                "Опишите ваш проект лендинга:\n"
                "• Какой продукт/услуга?\n"
                "• Целевая аудит
