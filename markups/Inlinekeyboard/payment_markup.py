from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


payment_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оплата', callback_data='payment')]
])
