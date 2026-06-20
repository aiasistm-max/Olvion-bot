import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

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

async def main():
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return
    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        welcome = f"👋 Добро пожаловать, {message.from_user.full_name}!\n\n Я - Профессор Олвион\nВаш интеллектуальный помощник\n\n🎯 Что я умею:\n• Создавать и управлять задачами\n• Оркестрировать ИИ-агентов\n• Сканировать сообщения\n• Вести CRM\n\n💡 Нажмите на кнопку внизу, чтобы начать!"
        await message.answer(welcome, reply_markup=get_main_menu())
    
    @dp.message()
    async def handle_buttons(message: Message):
        text = message.text
        
        if text == " Создать задачу":
            await message.answer(" Создание задачи\n\nОпишите вашу задачу:")
        elif text == "🤖 Мои агенты":
            await message.answer("🤖 Ваши ИИ-агенты:\n\n🎯 Джорлин - архитектура лендингов\n💰 CFO - финансовый анализ\n👥 Квалификатор - оценка лидов\n📱 SMM-Админ - соцсети\n🔍 Сканер - анализ сообщений")
        elif text == "📊 Проекты (CRM)":
            await message.answer("📊 Ваши проекты\n\nПока нет проектов. Создайте первую задачу!")
        elif text == "🔍 Сканер сообщений":
            await message.answer(" Сканер личных сообщений\n\nАгент читает чаты и присылает сводку:\n• кто ждет ответа\n• где деньги\n• где срочное\n\nФункция в разработке...")
        elif text == "⏱️ Активные задачи":
            await message.answer("⏱️ Активные задачи\n\nНет активных задач")
        elif text == "⚙️ Настройки":
            await message.answer(f"⚙️ Настройки\n\nВаш ID: {message.from_user.id}\nUsername: @{message.from_user.username or 'не указан'}")

async def run_bot():
    logger.info(" Bot started!")
    await main()

if __name__ == "__main__":
    asyncio.run(run_bot())
