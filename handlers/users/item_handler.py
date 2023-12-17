from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from loader import dp, db
from query_data.config import get_kategory, create_count_id


@dp.message_handler(text='🛍 Меню')
async def tovar(message: types.Message):
    create_count_id(message.from_user.id)
    inline_item = InlineKeyboardMarkup(row_width=2)
    for i in get_kategory():
        button = InlineKeyboardButton(text=i, switch_inline_query_current_chat=i)
        inline_item.insert(button)

    button_back = InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_menu')
    inline_item.add(button_back)
    await message.answer('Выберите Нужную себе Категорию', reply_markup=ReplyKeyboardRemove())
    await message.delete()
    await message.answer("Нажмите", reply_markup=inline_item)
    db.execute("delete from item where count = 0", commit=True)



