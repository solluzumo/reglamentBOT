import aiogram
from aiogram import types
import search
import keyboards
import classes as titles
from aiogram.types import InlineKeyboardMarkup
import json
import asyncio
async def send_reply(bot: aiogram.Bot,
                     object: types.Message,
                     parsed_title: titles.Title,
                     cluster:dict[str,str]|dict[str,None]|None,
                     is_cluster:bool)->None:
    """
    Эта функция получает данные из функции process_title и отправляет их пользователю.
    :param object: types.Message, объект на который 'отвечает' бот,
    :param parsed_title: classes.titles.Title,
    :param cluster:dict[str,str],
    :param is_cluster:bool
    :return:None
    """

    keyboard, titles = await process_title(parsed_title,cluster,is_cluster)
    total_buttons = sum(len(row) for row in keyboard.inline_keyboard)
    if not is_cluster:
        if parsed_title.photo:
            keyboard = keyboards.insert_photos(keyboard,parsed_title)
        if parsed_title.table:
            keyboard = keyboards.insert_tables(keyboard,parsed_title)
        if parsed_title.reglament.glossary:
            keyboard = keyboards.insert_glossary(keyboard)

    keyboard = keyboards.insert_cancel(keyboard)
    message_reply_text = (
        f"🔹 По вашему запросу найден следующий пункт:\n{parsed_title.title_name}\n\n"
        f"🔹 Из регламента:\n\n{parsed_title.reglament.full_reg_name}\n\n"
        f"{' '.join(titles)}\n\n"
    )

    if is_cluster:
        message_reply_text = f"По вашему запросу найдены следующие пункты:\n\n{' '.join(titles)}\n\n"

    if total_buttons > 2:
        message_reply_text += f"Некоторые подпункты слишком объемные, поэтому выберите пожалуйста один из них:\n"
    if len(message_reply_text) > 4096:
        for x in range(0, len(message_reply_text), 4096):
            await bot.send_message(object.chat.id, message_reply_text[x:x + 4096])
            await asyncio.sleep(3)
        await bot.send_message(object.chat.id, "Чтобы вернуться назад, посмотреть другие пункты или увидеть глоссарий, воспользуйтесь клавиатурой:\n", reply_markup=keyboard)
    else:
        await bot.send_message(object.chat.id, message_reply_text, reply_markup=keyboard)


    return None


async def process_title(parsed_title: titles.Title,
                        cluster:dict[str,str]|None,
                        is_cluster:bool)->(InlineKeyboardMarkup,list[str]):
    """
    Эта функция формирует данные для создания клавиатуры, текста сообщения, а так же приложения к заголовкам(фото и таблицы),
    обращаясь к тексту регламента,представленного в виде словаря и файлу accordance.txt.
    :param parsed_title: classes.titles.Title
    :param cluster:dict[str,str]
    :param is_cluster:bool
    :return: (InlineKeyboardMarkup,list[str])
    """

    current_root = parsed_title.current_root

    if is_cluster:
        current_root = cluster

    complex_titles = []
    accordance_list = [el.split('~~')[1] for el in open("static/text/accordance", encoding="utf-8").read().split('\n')]
    all_together = []
    for text in current_root:
        if not isinstance(text,dict):
            if not text.strip() in accordance_list:
                all_together.append(f"\n🔸{text.strip()}\n")

        else:
            for item, value in text.items():
                if item.strip() in accordance_list:
                    title = item.strip()
                    id = search.find_index_by_line(title)
                    line = search.find_line_by_index(id)
                    data = json.loads(
                        open(f"static/text/reglaments/{line.split('~~')[2].strip()}", encoding="utf-8").read())
                    title_object = titles.pars_string_title(line, data)
                    complex_titles.append(title_object)


    if not isinstance(current_root, list):
        for title in current_root:
            if title.strip() in accordance_list:
                title = title.strip()
                id = search.find_index_by_line(title)
                line = search.find_line_by_index(id)
                data = json.loads(open(f"static/text/reglaments/{line.split('~~')[2].strip()}", encoding="utf-8").read())
                title_object = titles.pars_string_title(line,data)
                complex_titles.append(title_object)

    if complex_titles:
        # Получаю список заголовков, которые входят в клавиатуру(их значения это другие словари)
        showing_complex = [f"\n🔸{element.title_name[:70]}...\n" for element in complex_titles]

        all_together = all_together+showing_complex


    keyboard = keyboards.create_main_keyboard(complex_titles)
    return keyboard, all_together
