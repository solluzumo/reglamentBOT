from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_main_keyboard(titles_and_indexes):
    keyboard = InlineKeyboardMarkup(row_width=1)

    for index,title in titles_and_indexes:
        if title!='Назад':
            button = InlineKeyboardButton(text=title, callback_data=f"main_key:{index}")
            keyboard.insert(button)
    cancel_data = titles_and_indexes[0]

    button_back = InlineKeyboardButton(text=cancel_data[1], callback_data=f"main_key:back{cancel_data[0]}")
    keyboard.insert(button_back)

    return keyboard