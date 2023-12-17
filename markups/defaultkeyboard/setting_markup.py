from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='🔄 Изменить имю'),
     KeyboardButton(text='🔄 Изменить номер')],
    [KeyboardButton(text='🔚 Главный меню')]
])

