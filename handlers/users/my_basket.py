from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.config import ADMINS
from loader import dp
from markups.defaultkeyboard.menu_markup import oformit_zakaz, menu_markup_def_admin, menu_markup_def, \
    oformit_zakaz_admin
from query_data.config import my_basket, delete_item, clear_korzina, get_count_korzina_item, increase, decrease, \
    get_korzina, item_count


@dp.message_handler(text='🛒 Моя Корзина')
async def basket(message: types.Message):
    await message.delete()
    i = my_basket(str(message.from_user.id))
    if len(i) == 0:
        if str(message.from_user.id) in ADMINS:
            await message.answer('Ваша корзина пусто!',
                                 reply_markup=menu_markup_def_admin)
        else:
            await message.answer('Ваша корзина пусто!',
                                 reply_markup=menu_markup_def)
    else:
        for j in i:
            await message.answer(
                f'<b>Название</b> - <i>{j[1]}</i>\n<b>Сумма</b> - {j[3]}KZT\n<b>Информация</b> - <i>{j[2]}</i>\n<b>Фото </b> - <a href="{j[5]}">{j[1]}</a>',
                disable_web_page_preview=True, reply_markup=product_markup(j[0], j[4]))
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton('Итог', callback_data='all_money')
        markup.add(btn)
        await message.answer(f"Что бы увидеть Итог\nНажмите 👇", reply_markup=markup)
        if str(message.from_user.id) in ADMINS:
            await message.answer('Хотите оформить заказ нажмите на\nОформить заказ 📑', reply_markup=oformit_zakaz_admin)
        else:
            await message.answer('Хотите оформить заказ нажмите на\nОформить заказ 📑', reply_markup=oformit_zakaz)


@dp.message_handler(text='🧹 Очистить корзину')
async def clear_basket(message: types.Message):
    await message.delete()
    delete_item(message.from_user.id)
    if str(message.from_user.id) in ADMINS:
        await message.answer('Ваша корзина очишена!', reply_markup=menu_markup_def_admin)
    else:
        await message.answer('Ваша корзина очишена!', reply_markup=menu_markup_def)


product_cb = CallbackData('product', 'id', 'action')


def product_markup(idx, count):
    global product_cb
    markup = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton('➖', callback_data=product_cb.new(id=idx, action='increase'))
    count_btn = InlineKeyboardButton(count, callback_data=product_cb.new(id=idx, action='count'))
    next_btn = InlineKeyboardButton('➕', callback_data=product_cb.new(id=idx, action='decrease'))
    delete_btn = InlineKeyboardButton('🗑 Удалить', callback_data=product_cb.new(id=idx, action='delete'))
    markup.row(back_btn, count_btn, next_btn)
    markup.add(delete_btn)

    return markup


@dp.callback_query_handler(product_cb.filter(action='count'))
@dp.callback_query_handler(product_cb.filter(action='increase'))
@dp.callback_query_handler(product_cb.filter(action='decrease'))
@dp.callback_query_handler(product_cb.filter(action='delete'))
async def korzina_btn(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    idx = callback_data['id']
    action = callback_data['action']
    if action == 'count':
        await callback.answer(f'Количество {get_count_korzina_item(callback.from_user.id, idx)}')

    elif action == 'delete':
        await callback.message.delete(), clear_korzina(callback.from_user.id, idx)
        users_id = []
        for i in get_korzina():
            users_id.append(i[2])
        if str(callback.from_user.id) in users_id:
            pass
        else:
            if str(callback.from_user.id) in ADMINS:
                await callback.message.answer('Главный меню', reply_markup=menu_markup_def_admin)
            else:
                await callback.message.answer('Главный меню', reply_markup=menu_markup_def)

    elif action == 'increase':
        if get_count_korzina_item(callback.from_user.id, idx) == 1:
            await callback.answer('Минимум до 1')
        else:
            increase(callback.from_user.id, idx)
            await callback.message.edit_reply_markup(product_markup(idx, get_count_korzina_item(callback.from_user.id, idx)))
            await callback.answer()

    else:
        item_c = item_count(idx)
        if get_count_korzina_item(callback.from_user.id, idx) == item_c:
            await callback.answer(f'Но этого предмета осталась только {item_c}', show_alert=True)
        else:
            decrease(callback.from_user.id, idx)
            await callback.message.edit_reply_markup(product_markup(idx, get_count_korzina_item(callback.from_user.id, idx)))
            await callback.answer()


@dp.callback_query_handler(text='all_money')
async def all_money(callback: types.CallbackQuery):
    money = int()
    i = my_basket(str(callback.from_user.id))
    for j in i:
        money += j[3] * j[4]
    await callback.answer(f'Итоговая сумма {money}KZT', show_alert=True)
