from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

set_tasks_button: KeyboardButton = KeyboardButton(text='Записать напоминалку')
delete_task_button: KeyboardButton = KeyboardButton(text='Удалить напоминалку')

# Создаем объект клавиатуры, добавляя в него кнопки
default_keybord: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[set_tasks_button, delete_task_button]],
                                    resize_keyboard=True)
