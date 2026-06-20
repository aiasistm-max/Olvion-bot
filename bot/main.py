import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

# Настройки
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Главное меню
def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
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
    return keyboard

# Создание бота
async def main():
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не установлен!")
        return
    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    # Обработчик /start
    @dp.message(Command("start"))
    async def cmd_start(message: Message):        welcome = f"""
👋 <b>Добро пожаловать, {message.from_user.full_name}!</b>

🤖 <b>Я - Профессор Олвион</b>
Ваш интеллектуальный помощник

🎯 <b>Что я умею:</b>
• Создавать и управлять задачами
• Оркестрировать ИИ-агентов
• Сканировать сообщения
• Вести CRM

💡 Нажмите на кнопку внизу, чтобы начать!
        """
        await message.answer(welcome, reply_markup=get_main_menu())
    
    # Обработчик кнопок
    @dp.message()
    async def handle_buttons(message: Message):
        text = message.text
        
        if text == "📝 Создать задачу":
            await message.answer("📝 <b>Создание задачи</b>\n\nОпишите вашу задачу:")
        
        elif text == "🤖 Мои агенты":
            await message.answer("""
🤖 <b>Ваши ИИ-агенты:</b>

🎯 <b>Джорлин</b> - архитектура лендингов
💰 <b>CFO</b> - финансовый анализ
👥 <b>Квалификатор</b> - оценка лидов
📱 <b>SMM-Админ</b> - соцсети
🔍 <b>Сканер</b> - анализ сообщений
            """)
        
        elif text == "📊 Проекты (CRM)":
            await message.answer("📊 <b>Ваши проекты</b>\n\nПока нет проектов. Создайте первую задачу!")
        
        elif text == "🔍 Сканер сообщений":
            await message.answer("""
🔍 <b>Сканер личных сообщений</b>

Агент читает чаты и присылает сводку:
• кто ждет ответа
• где деньги
• где срочное

Функция в разработке...
            """)
                elif text == "⏱️ Активные задачи":
            await message.answer("⏱️ <b>Активные задачи</b>\n\nНет активных задач")
        
        elif text == "⚙️ Настройки":
            await message.answer(f"""
⚙️ <b>Настройки</b>

Ваш ID: <code>{message.from_user.id}</code>
Username: @{message.from_user.username or 'не указан'}
            """)
    
    # Запуск
    logger.info("🚀 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
