from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

location_markup = ReplyKeyboardMarkup(resize_keyboard=True)
location = KeyboardButton('Location', request_location=True)
location_markup.add(location)
location_markup.add("⬅️ Назад")
