import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import ContextTypes
# Не импортируйте из bot!
# Если необходим токен, импортируйте его из config.py:
# from config import TELEGRAM_TOKEN

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Це Telegram-бот з інтеграцією ChatGPT. Обери одну з команд: /random, /gpt, /talk або /quiz.")
# Функция-заглушка для вызова ChatGPT (потом замените на реальный API вызов)
def get_random_fact_from_chatgpt() -> str:
    prompt = "Розкажи мені цікавий факт."
    # Здесь нужно сделать запрос к OpenAI API
    return "Ось цікавий факт: Земля обертається навколо своєї осі."

async def random_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправляем изображение
    image_path = os.path.join("assets", "random_fact.png")
    if os.path.exists(image_path):
        await update.message.reply_photo(photo=InputFile(image_path))
    else:
        await update.message.reply_text("Зображення не знайдено.")

    # Получаем факт от ChatGPT (заглушка)
    fact = get_random_fact_from_chatgpt()

    # Кнопки
    keyboard = [
        [
            InlineKeyboardButton("Закінчити", callback_data="finish"),
            InlineKeyboardButton("Хочу ще факт", callback_data="random_again"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text=fact, reply_markup=reply_markup)


# Заглушка для ChatGPT интерфейса
def get_response_from_chatgpt(user_text: str) -> str:
    # Здесь должен быть вызов к OpenAI API
    return f"Відповідь ChatGPT на: {user_text}"


async def gpt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_path = os.path.join("assets", "gpt_interface.png")
    if os.path.exists(image_path):
        await update.message.reply_photo(photo=InputFile(image_path))
    else:
        await update.message.reply_text("Зображення не знайдено.")

    # Проверяем, есть ли текст после команды
    if update.message.text and len(update.message.text.split()) > 1:
        # Извлекаем текст после команды /gpt
        user_text = update.message.text.partition(" ")[2]
        response = get_response_from_chatgpt(user_text)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Будь ласка, надішліть текст після команди /gpt.")
