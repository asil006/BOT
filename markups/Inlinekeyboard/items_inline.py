from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

product_cb = CallbackData('product', 'id', 'count', 'action')


def add_markup(id, count, korzina):
    global product_cb
    id = int(id)
    ids = []
    for i in korzina:
        ids.append(i[1])
    if id in ids:
        add_str = '📥 Обновить корзину'
    else:
        add_str = '📥 Добавить в корзину'
    markup = InlineKeyboardMarkup()
    minus_btn = InlineKeyboardButton('➖', callback_data=product_cb.new(id=id, count=count, action='minus'))
    count_btn = InlineKeyboardButton(count, callback_data=product_cb.new(id=id, count=count, action='_'))
    plus_btn = InlineKeyboardButton('➕', callback_data=product_cb.new(id=id, count=count, action='plus'))
    add_btn = InlineKeyboardButton(text=add_str, callback_data=product_cb.new(id=id, count=count, action='add'))
    back_btn = InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_inline')
    markup.row(minus_btn, count_btn, plus_btn)
    markup.row(add_btn)
    markup.add(back_btn)
    return markup
