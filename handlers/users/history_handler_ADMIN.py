from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from loader import dp, db
from markups.Inlinekeyboard.history_markup import markup_history_admin
from markups.defaultkeyboard.menu_markup import oformit_zakaz, oformit_zakaz_admin
from states.history_state import History


@dp.message_handler(text='🗒 История заказов[ADMIN]')
async def top_products(message: types.Message):
    await message.delete()
    history = db.execute(f'select distinct o.date from oformlenie o join registration r on r.id = o.user_id')
    if not history:
        if str(message.from_user.id) in ADMINS:
            await message.answer('В истории ничего!', reply_markup=oformit_zakaz_admin)
        else:
            await message.answer('В истории ничего!', reply_markup=oformit_zakaz)
    else:
        await message.answer('Выберите:', reply_markup=markup_history_admin)


@dp.callback_query_handler(text='waiting[ADMIN]')
async def waiting(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    dates = db.execute(f'select distinct o.date from oformlenie o join registration r on r.id = o.user_id where check_zakaz == False', fetchall=True)
    markup = InlineKeyboardMarkup()
    if not dates:
        await callback.message.answer('В истории ничего!', reply_markup=markup_history_admin)
    else:
        for i in dates:
            for j in i:
                markup.insert(InlineKeyboardButton(text=j, callback_data=j))
        markup.add(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_wait'))
        await callback.message.answer('Выберите дату', reply_markup=markup)


@dp.callback_query_handler(text='history[ADMIN]')
async def waiting(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    dates = db.execute(f'select distinct o.date from oformlenie o join registration r on r.id = o.user_id where check_zakaz == True', fetchall=True)
    markup = InlineKeyboardMarkup()
    if not dates:
        await callback.message.answer('В ожидании ничего!', reply_markup=markup_history_admin)
    else:
        for i in dates:
            for j in i:
                markup.insert(InlineKeyboardButton(text=j, callback_data=j))
        markup.add(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_wait'))
        await callback.message.answer('Выберите дату', reply_markup=markup)
        await History.time_admin.set()


@dp.message_handler(state=History.time_admin)
async def histoy_admin(message: types.Message):
    await message.answer('Ok')
