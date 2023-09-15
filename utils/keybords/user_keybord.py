from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

set_tasks_button: KeyboardButton = KeyboardButton(text='Записать напоминалку')
# delete_task_button: KeyboardButton = KeyboardButton(text='Удалить напоминалку')
# edit_task_button: KeyboardButton = KeyboardButton(text='Редактировать напоминалку')


# Создаем объект клавиатуры, добавляя в него кнопки
default_keybord: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[set_tasks_button]],
                                    resize_keyboard=True)
