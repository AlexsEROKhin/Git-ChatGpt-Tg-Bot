import os
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных из файла .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set in environment variables")
