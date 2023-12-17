from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_markup_def = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='🛍 Меню')],
    [KeyboardButton(text='🛒 Моя Корзина'),
     KeyboardButton(text='📩 Мои промокоды')],
    [KeyboardButton(text='ℹ️ Информация'),
     KeyboardButton(text='☎️ Обратная связь')],
    [KeyboardButton(text='⚙️ Настройки')]
])

menu_markup_def_admin = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='🛍 Меню')],
    [KeyboardButton(text='🛒 Моя Корзина'),
     KeyboardButton(text='📩 Мои промокоды')],
    [KeyboardButton(text='ℹ️ Информация'),
     KeyboardButton(text='☎️ Обратная связь')],
    [KeyboardButton(text='⚙️ Настройки'),
     KeyboardButton(text='➕ Добавить товар[ADMIN]')]
])

oformit_zakaz = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='📑 Оформить заказ'),
     KeyboardButton(text='🗒 История моих покупок')],
    [KeyboardButton(text='🧹 Очистить корзину'),
     KeyboardButton(text='🔚 Главный меню')]
])
oformit_zakaz_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='📑 Оформить заказ'),
     KeyboardButton(text='🗒 История заказов[ADMIN]')],
    [KeyboardButton(text='🧹 Очистить корзину'),
     KeyboardButton(text='🔚 Главный меню')]
])
