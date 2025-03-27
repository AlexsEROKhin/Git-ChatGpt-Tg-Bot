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
        with open(image_path, "rb") as photo:
            await update.message.reply_photo(photo=InputFile(photo, filename="random_fact.png"))
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


# Словарь, сопоставляющий имя личности с соответствующим промптом для ChatGPT
PERSONALITIES = {
    "Альберт Ейнштейн": "Веди діалог, відповідаючи як Альберт Ейнштейн.",
    "Ілон Маск": "Веди діалог, відповідаючи як Ілон Маск.",
    "Марк Цукерберг": "Веди діалог, відповідаючи як Марк Цукерберг."
}


async def talk_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /talk.
    При вызове отправляет изображение (если оно имеется) и предлагает пользователю выбрать
    одну из персон через inline-кнопки. Выбранная личність сохраняется в context.user_data для дальнейшей работы.
    """
    # Формируем путь к изображению для режима "діалог з відомою особистістю"
    image_path = os.path.join("assets", "talk_persona.png")

    # Проверяем наличие файла изображения
    if os.path.exists(image_path):
        # Отправляем изображение
        await update.message.reply_photo(photo=InputFile(image_path))
    else:
        # Если изображения нет – отправляем текстовое уведомление
        await update.message.reply_text("Зображення для діалогу з особистістю не знайдено.")

    # Создаем inline-кнопки для выбора каждой личности.
    # Для каждой личности создаем отдельный ряд с кнопкой.
    keyboard_buttons = []
    for name in PERSONALITIES.keys():
        # Формируем callback_data в формате "talk:Имя"
        button = InlineKeyboardButton(text=name, callback_data=f"talk:{name}")
        keyboard_buttons.append([button])  # Каждая кнопка в отдельном ряду

    # Формируем объект разметки клавиатуры
    reply_markup = InlineKeyboardMarkup(keyboard_buttons)

    # Отправляем сообщение с предложением выбора личности
    await update.message.reply_text("Будь ласка, оберіть особистість для діалогу:", reply_markup=reply_markup)


async def talk_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик callback_query для команды /talk.
    При выборе пользователем кнопки извлекается выбранная особистість и соответствующий промпт.
    Выбранный промпт сохраняется в context.user_data, а сообщение редактируется для подтверждения выбора.
    """
    query = update.callback_query
    # Подтверждаем получение callback
    await query.answer()

    callback_data = query.data  # Ожидаем формат "talk:Имя"
    if callback_data.startswith("talk:"):
        # Извлекаем имя личности после двоеточия
        selected_personality = callback_data.split(":", 1)[1]
        # Получаем соответствующий промпт из словаря PERSONALITIES
        prompt = PERSONALITIES.get(selected_personality, "")

        # Сохраняем выбранный промпт в context.user_data для дальнейшей обработки
        context.user_data["talk_prompt"] = prompt
        # Также сохраняем имя выбранной личности (для логирования или дальнейшей обработки)
        context.user_data["selected_personality"] = selected_personality

        # Редактируем сообщение, чтобы уведомить пользователя о выборе
        new_text = (
            f"Обрано: {selected_personality}.\n"
            f"Тепер введіть ваше повідомлення для діалогу з {selected_personality}.\n"
            f"(Для завершення діалогу використовуйте команду /start)"
        )
        await query.edit_message_text(text=new_text)
    else:
        # Если формат callback_data не соответствует ожиданиям, сообщаем об ошибке
        await query.edit_message_text(text="Невірний вибір, спробуйте ще раз.")