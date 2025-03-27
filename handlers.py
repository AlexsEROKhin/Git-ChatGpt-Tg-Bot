from telegram import Update
from telegram.ext import ContextTypes
# Не импортируйте из bot!
# Если необходим токен, импортируйте его из config.py:
# from config import TELEGRAM_TOKEN

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Це Telegram-бот з інтеграцією ChatGPT. Обери одну з команд: /random, /gpt, /talk або /quiz.")

