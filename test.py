import json
import difflib
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from fuzzywuzzy import fuzz

# Здесь вы можете предоставить данные заголовки и соответствующие тексты

# Ваш токен бота
TOKEN = ""

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())



# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Введите заголовок, и я постараюсь найти соответствующий текст.")

# Обработчик ввода заголовка пользователем
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def process_title(message: types.Message):
    data = json.loads(open("text/fromprompt", encoding="utf-8").read())

    user_title = message.text.lower()
    best_match = None
    best_match_ratio = 0

    for title in data.keys():
        ratio = fuzz.partial_ratio(user_title, title.lower())
        if ratio > best_match_ratio:
            best_match_ratio = ratio
            best_match = title

    if best_match:
        formatted_text = "\n".join(f"⦁ {text.lstrip('-')}" for text in data[best_match] if text.strip())
        await message.reply(f"Найден соответствующий заголовок: '{best_match}':\n\n{formatted_text}",
                            parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply("Заголовок не найден. Попробуйте ввести другой заголовок.")

if __name__ == "__main__":
    # Запуск бота
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
#находить сначал без fuzzy wuzzy, если не удаётся найти точное совпадение, то уже подрубаем fuzzy wuzzy
#выводить подпункты по желанию пользователя(через клаву)
#выводить выбранный из трёх похожих пунктов (через клаву)
#про вопросы коллег где и какую инфу искать: сделать по каждому регламенту на основе заколовков и содержания несколько уточняющих категорий(типо инструкция по монтажу на буровой, инструкция по гидравлическим испытаниям ПВО и т.п.) (такой же поиск по заголовкам)
#если не нахожу по заголовкам, то:
#1)с помощью fuzzywuzzy нахожу 10 похожих заголовков и там ищу в каждом пункте/подпункте
#2)перебираю