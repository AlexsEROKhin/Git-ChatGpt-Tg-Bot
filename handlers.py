from telegram import Update
from telegram.ext import ContextTypes, Application

from bot import TELEGRAM_TOKEN


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Це Telegram-бот з інтеграцією ChatGPT. Обери одну з команд: /random, /gpt, /talk або /quiz.")

from telegram.ext import CommandHandler
from handlers import start_handler

def build_app() -> Application:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    return app
