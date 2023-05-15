from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# Создаем объекты кнопок
today_button: KeyboardButton = KeyboardButton(text='Узнать дату на сегодня')
set_tasks_button: KeyboardButton = KeyboardButton(text='Записать список задач на день')
delete_task_button: KeyboardButton = KeyboardButton(text='Удалить задачу')
set_day_button: KeyboardButton = KeyboardButton(text='Задать дату')
delete_day_button: KeyboardButton = KeyboardButton(text='Удалить дату')


# Создаем объект клавиатуры, добавляя в него кнопки
default_keybord: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[set_tasks_button, delete_task_button],
                                              [today_button, set_day_button, delete_day_button]],
                                    resize_keyboard=True)


# Создаем объекты инлайн-кнопок
big_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 1',
    callback_data='big_button_1_pressed')

big_button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 2',
    callback_data='big_button_2_pressed')

# Создаем объект инлайн-клавиатуры
inline_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_1],
                     [big_button_2]])

