from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_markup = ReplyKeyboardMarkup(resize_keyboard=True)
contact = KeyboardButton('Contact', request_contact=True)
contact_markup.add(contact)
