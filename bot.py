import os
from dotenv import load_dotenv
from telegram.ext import Application

load_dotenv()  # загрузка переменных из файла .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set in environment variables")

def build_app() -> Application:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    return app

if __name__ == '__main__':
    app = build_app()
    print("Bot successfully built!")
    app.run_polling()
