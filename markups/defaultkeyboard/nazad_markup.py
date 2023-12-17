from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, keyboard=[
    [KeyboardButton(text='⬅️ Назад')]
])
