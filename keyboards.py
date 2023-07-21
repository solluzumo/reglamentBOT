from aiogram import types


def get_titles_correction(titles):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for title in titles:
        button = types.InlineKeyboardButton(text=title, callback_data=f'correction_title:{title}')
        keyboard.add(button)

    return keyboard

