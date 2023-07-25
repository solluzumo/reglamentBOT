import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from fuzzywuzzy import fuzz
from aiogram import executor
from keyboards import create_main_keyboard
import search
import titles
# Ваш токен бота
TOKEN = "5781618054:AAHAcNTbY0GC391C5JU76O1yGLiNCoxtg1U"

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def send_reply(object: types.Message):
    keyboard, titles = await process_title()
    total_buttons = sum(len(row) for row in keyboard.inline_keyboard)

    if keyboard:
        message_reply_text = f"По вашему запросу нашел следующий пункт:\n{parsed_title.title_name}\n\n{' '.join(titles)}\n\n"

        if total_buttons > 1:
            message_reply_text += f"Некоторые подпункты слишком объемные, поэтому выберите пожалуйста один из них:\n"

        await object.reply(message_reply_text, reply_markup=keyboard)
    return None


async def process_title():
    #Заполнение данных для кнопки 'Назад'
    current_title_index = parsed_title.id
    titles_and_indexes = [[str(current_title_index), 'Назад']]
    current_root = parsed_title.current_root

    all_together = [f"\n{text.lstrip('-')}\n" for text in current_root]
    complex_titles = None

    if not isinstance(current_root,list):
        complex_titles = [text.rstrip() for text in current_root if isinstance(current_root[text], (dict, list))]

    if complex_titles:
        #Получаю список заголовков, которые не входят в клавиатуру(их значения это не другие словари)
        all_together = [element.strip() for element in all_together if not element.strip() in complex_titles]

        #Получаю список заголовков, которые входят в клавиатуру(их значения это другие словари)
        showing_complex = [f"\n{element[:70]}...\n" for element in complex_titles]

        all_together = all_together + showing_complex
        titles_and_indexes = titles_and_indexes+[[str(search.find_index_by_line(complex_title)), complex_title]
                              for complex_title in complex_titles]
    keyboard = create_main_keyboard(titles_and_indexes)
    return keyboard,all_together

stored_password = "123"
def check_user_id(func):
    async def wrapper(message: types.Message, *args, **kwargs):
        with open('text/users', 'r', encoding='utf-8') as file:
            users_list = file.read().split('\n')
            if str(message.from_user.id) in users_list:
                return await func(message)
            else:
                await message.reply("Доступ запрещен. Введите пароль через команду /password.Например:\n"
                                    "/password 12345")
                return None
    return wrapper
@dp.message_handler(commands=['password'])
async def password_handler(message: types.Message):
    # Получаем текст сообщения пользователя и разделяем его на команду и пароль
    command, password = message.text.split(maxsplit=1)
    password = password.strip()
    with open('text/users', 'r+', encoding='utf-8') as file:
        # Проверка пароля
        if password == stored_password:
            file.write(str(message.from_user.id) + "\n")
            await message.reply("Пароль верный. Доступ разрешен.")
        else:
            await message.reply("Пароль неверный. Доступ запрещен.")



# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Введите заголовок, и я постараюсь найти соответствующий текст. Если вы впервые пользуетесь ботом, то"
                        "введите пароль через команду /password.Например:\n /password 12345")

# Обрабка текстовых сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
@check_user_id
async def main(message: types.Message):
    global data
    global parsed_title

    #Получаем заголовки, среди которых будет производиться поиск
    with open('text/accordance', 'r', encoding='utf-8') as file:
        accordance_list = [line.strip() for line in file]

    #Поиск совпадения запроса пользователя с заголовками
    best_match = None
    best_match_line = accordance_list[0]
    user_title = message.text.lower()
    best_match_ratio = 0
    if not best_match:
        for line in accordance_list:
            info = line.split('/')
            title = info[1]
            file_name = info[4]
            ratio = fuzz.partial_ratio(user_title, title.lower())
            if ratio > best_match_ratio:
                best_match_ratio = ratio
                best_match_line = line

    data = json.loads(open(f"text/reglaments/{file_name}", encoding="utf-8").read())
    parsed_title = titles.pars_string_title(best_match_line,data)
    await send_reply(message)


#Обработка клавиатуры
@dp.callback_query_handler(lambda c: c.data.startswith('main_key:'))
async def correction_title_handler(callback_query: types.CallbackQuery):
    global parsed_title
    title_index = callback_query.data.split(':')[1]
    #Обрабатываем кнопку назад
    if 'back' in title_index:
        #Находим заголовок(ключ), в который входит текущий пункт.
        if parsed_title.before_key == '/start':
            await callback_query.message.reply(f"Вы находитесь в регламенте '{parsed_title.reglament.reg_name}")
            return None
        chosen_title = search.find_line_by_index(parsed_title.before_key)
    else:
        chosen_title = search.find_line_by_index(title_index)

    parsed_title = titles.pars_string_title(chosen_title,data)

    await send_reply(callback_query.message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

