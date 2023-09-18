from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

set_date_button: KeyboardButton = KeyboardButton(text='Задать дату-время')

set_tasks_button: KeyboardButton = KeyboardButton(text='Записать напоминалку')
delete_task_button: KeyboardButton = KeyboardButton(text='Удалить напоминалку')
edit_task_button: KeyboardButton = KeyboardButton(text='Редактировать напоминалку')

# Создаем объект клавиатуры, добавляя в него кнопки
default_keybord: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[set_tasks_button, delete_task_button, edit_task_button]],
    resize_keyboard=True
)

origin_keybord: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[set_date_button]],
    resize_keyboard=True
)
