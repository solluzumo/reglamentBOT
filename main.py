from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import difflib
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
API_TOKEN = "5781618054:AAGzAr-MbhK26CNH7NpXvtTTPBEuUiea0xs"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


#Присылает пользователю приветствие
# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Введите заголовок, и я постараюсь найти соответствующий текст.")

# Обработчик ввода заголовка пользователем
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def process_title(message: types.Message):
    data = open("text/reglaments/reg1", encoding="utf-8").read()
    user_title = message.text
    match = difflib.get_close_matches(user_title, data.keys(), n=1, cutoff=0.6)
    if match:
        # Если нашли соответствующий заголовок, отправляем текст
        title_match = match[0]
        text = data[title_match]
        await message.reply(f"Найден соответствующий заголовок: '{title_match}'. Вот текст:\n\n{text}",
                            parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply("Заголовок не найден. Попробуйте ввести другой заголовок.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)