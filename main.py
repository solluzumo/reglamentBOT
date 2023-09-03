import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from fuzzywuzzy import fuzz
from aiogram import executor
import os
import keyboards
import title_handler
import search
import classes as titles


TOKEN = os.getenv("token")

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


stored_password = "123"
def check_user_id(func):
    async def wrapper(message: types.Message):
        with open('static/text/users', 'r', encoding='utf-8') as file:
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
    with open('static/text/users', 'r+', encoding='utf-8') as file:
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
    global cluster
    global is_cluster
    is_cluster = True
    cluster = {}
    #Получаем заголовки, среди которых будет производиться поиск
    with open('static/text/accordance', 'r', encoding='utf-8') as file:
        accordance_list = [line.strip() for line in file]

    user_title = message.text.lower()

    matches = []

    for line in accordance_list:
        info = line.split('~~')
        title = info[1]
        ratio = fuzz.partial_ratio(user_title, title.lower())
        matches.append([line, ratio])

    # Сортируем соответствия по убыванию коэффициента сходства
    matches = sorted(matches, key=lambda x: x[1], reverse=True)

    # Выбираем первые два заголовка с наибольшим сходством
    best_matches = [matche[0] for matche in matches[:5]]
    for best_match in best_matches:
        parsed_title_info = best_match.split('~~')
        parsed_title_file = json.loads(open(f'static/text/reglaments/{parsed_title_info[2]}',encoding="utf-8").read())
        parsed_title = titles.pars_string_title(best_match, parsed_title_file)
        cluster[parsed_title.title_name] = parsed_title.current_root


    await title_handler.send_reply(bot,message,parsed_title,cluster,is_cluster)


#Обработка клавиатуры
@dp.callback_query_handler(lambda c: c.data.startswith('main_key:'))
async def correction_title_handler(callback_query: types.CallbackQuery):
    global parsed_title
    global is_cluster
    global cluster

    cluster = None
    is_cluster = False
    title_index = callback_query.data.split(':')[1]

    #Обрабатываем кгнопку назад
    if 'back' in title_index:
        #Находим заголовок(ключ), в который входит текущий пункт.
        if parsed_title.before_key == '/start':
            await callback_query.message.reply(f"Вы находитесь в регламенте\n\n{parsed_title.reglament.full_reg_name}")
        chosen_title = search.find_line_by_index(parsed_title.before_key)
    else:
        chosen_title = search.find_line_by_index(title_index)


    data = json.loads(open(f'static/text/reglaments/{chosen_title.split("~~")[2].rstrip()}', encoding="utf-8").read())

    parsed_title = titles.pars_string_title(chosen_title, data)

    await title_handler.send_reply(bot,callback_query.message,parsed_title,cluster,is_cluster)

@dp.callback_query_handler(lambda c: c.data.startswith('glossary_key'))
async def correction_title_handler(callback_query: types.CallbackQuery):
    global is_cluster
    is_cluster = False
    if parsed_title.reglament.glossary:
        keyboard = keyboards.create_main_keyboard(None)
        keyboard = keyboards.insert_cancel(keyboard)
    await callback_query.message.reply(f"Глоссарий для данного регламента:\n\n{parsed_title.reglament.glossary}")

@dp.callback_query_handler(lambda c: c.data.startswith("send_image"))
async def send_image(callback_query: types.CallbackQuery):
    index = callback_query.data.split(':')[1]
    photo = open(f'static/images/{parsed_title.id}/{parsed_title.photo[int(index)]}', 'rb')

    await bot.send_photo(callback_query.from_user.id, photo)


@dp.callback_query_handler(lambda c: c.data.startswith("send_table"))
async def send_table(callback_query: types.CallbackQuery):
    index = callback_query.data.split(':')[1]

    table = open(f'static/tables/{parsed_title.id}/{parsed_title.table[int(index)]}', 'r', encoding="utf-8").read()

    if parsed_title.reglament.glossary:
        keyboard = keyboards.create_main_keyboard(None)
        keyboard = keyboards.insert_cancel(keyboard)
    await callback_query.message.reply(f"Таблица:\n\n{table}",reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

