from telegram.ext import Application, CommandHandler
from config import TELEGRAM_TOKEN  # импорт из config.py
from handlers import start_handler  # импорт обработчиков

def build_app() -> Application:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    return app

if __name__ == '__main__':
    app = build_app()
    print("Bot successfully built!")
    app.run_polling()

