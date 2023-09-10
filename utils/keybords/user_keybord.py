from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

set_tasks_button: KeyboardButton = KeyboardButton(text='Записать напоминалку')
delete_task_button: KeyboardButton = KeyboardButton(text='Удалить напоминалку')
edit_task_button: KeyboardButton = KeyboardButton(text='Редактировать напоминалку')

date_button: KeyboardButton = KeyboardButton(text='Выбрать дату')

# Создаем объект клавиатуры, добавляя в него кнопки
default_keybord: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[set_tasks_button, delete_task_button, edit_task_button]],
                                    resize_keyboard=True)


first_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[date_button]],
                                                          resize_keyboard=True)
