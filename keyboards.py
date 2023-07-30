from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from classes import Title
def create_main_keyboard(titles:list[Title]|None)->InlineKeyboardMarkup:
    """
    Функция создает клавиатуру для заголовков, у которых есть подзаголовки, так же кнопку Назад и кнопку Глоссарий
    :param titles_and_indexes: list[Title] or None
    """

    keyboard = InlineKeyboardMarkup(row_width=1)
    if titles:
        for title in titles:
            button = InlineKeyboardButton(text=title.title_name, callback_data=f"main_key:{title.id}")
            keyboard.insert(button)
    return keyboard

def insert_photos(keyboard:InlineKeyboardMarkup,parsed_title:Title)->InlineKeyboardMarkup:
    for index in range(len(parsed_title.photo)):
        button = InlineKeyboardButton(text=f"Фото номер {index+1}", callback_data=f"send_image:{index}")
        keyboard.insert(button)
    return keyboard

def insert_tables(keyboard:InlineKeyboardMarkup,parsed_title:Title)->InlineKeyboardMarkup:
    for index in range(len(parsed_title.table)):
        button = InlineKeyboardButton(text=f"Таблица номер {index+1}", callback_data=f"send_table:{index}")
        keyboard.insert(button)
    return keyboard

def insert_glossary(keyboard:InlineKeyboardMarkup)->InlineKeyboardMarkup:
    button_glossary = InlineKeyboardButton(text="Глоссарий", callback_data="glossary_key")
    keyboard.insert(button_glossary)
    return keyboard

def insert_cancel(keyboard:InlineKeyboardMarkup)->InlineKeyboardMarkup:
    cancel_button = InlineKeyboardButton(text='Назад', callback_data=f"main_key:back")
    keyboard.insert(cancel_button)
    return keyboard