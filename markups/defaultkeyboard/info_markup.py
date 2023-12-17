from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='📍Локация АР shop'),
     KeyboardButton(text='🔚 Главный меню')]
])
