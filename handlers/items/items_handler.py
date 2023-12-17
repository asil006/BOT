from aiogram import types

from data.config import ADMINS
from loader import dp, bot
from markups.Inlinekeyboard.items_inline import add_markup, product_cb
from markups.defaultkeyboard.menu_markup import menu_markup_def, menu_markup_def_admin
from query_data.config import get_item, add_my_basket, update_plus_count, update_minus_count, update_count, \
    item_count, db, get_korzina


def item():
    name = []
    try:
        fetchall = db.execute("""select name from item""", fetchall=True)
        for i in fetchall:
            for j in i:
                name.append(j)
        return name
    except Exception as err:
        print(err)


@dp.message_handler(text=item())
async def item(message: types.Message):
    await message.delete()
    item_name = message.text
    i = get_item(item_name)
    item_id = i[0]
    count = 1
    for j in get_korzina():
        if j[2] == str(message.from_user.id) and j[1] == item_id:
            count = j[3]
    if str(message.from_id) in ADMINS:
        await message.answer_photo(photo=i[6],
                                   caption=f"{i[2]} - {i[4]}KZT\n\n{i[3]}\n\nОсталось🔄 - {i[5]}",
                                   reply_markup=add_markup(item_id, count, get_korzina()))
    else:
        await message.answer_photo(photo=i[6],
                                   caption=f"{i[2]} - {i[4]}KZT\n\n{i[3]}",
                                   reply_markup=add_markup(item_id, count, get_korzina()))


@dp.callback_query_handler(product_cb.filter(action='_'))
@dp.callback_query_handler(product_cb.filter(action='minus'))
@dp.callback_query_handler(product_cb.filter(action='plus'))
@dp.callback_query_handler(product_cb.filter(action='add'))
async def add(callback: types.CallbackQuery, callback_data: dict):
    action = callback_data['action']
    item_id = callback_data['id']
    count = callback_data['count']
    count = int(count)
    if action == 'add':
        await callback.message.delete()
        update_count(callback.from_user.id)
        add_my_basket(item_id, callback.from_user.id, count)
        if str(callback.from_user.id) in ADMINS:
            await callback.message.answer("✅ Успешно добавлено\nОформить заказ можете в разделе Моя корзина",
                                          reply_markup=menu_markup_def_admin)
        else:
            await callback.message.answer("✅ Успешно добавлено\nОформить заказ можете в разделе Моя корзина",
                                          reply_markup=menu_markup_def)
        await callback.answer()

    elif action == 'plus':
        item_c = item_count(item_id)
        if count == item_c:
            await callback.answer(f'Но этого предмета осталась только {item_c}', show_alert=True)
        else:
            count += 1
            update_plus_count(callback.from_user.id)
            await bot.edit_message_reply_markup(callback.message.chat.id,
                                                callback.message.message_id,
                                                inline_message_id=callback.inline_message_id,
                                                reply_markup=add_markup(item_id, count, get_korzina()))
            await callback.answer()

    elif action == 'minus':
        if count == 1:
            await callback.answer('Минимум до 1')
        else:
            count -= 1
            update_minus_count(callback.from_user.id)
            await bot.edit_message_reply_markup(callback.message.chat.id,
                                                callback.message.message_id,
                                                inline_message_id=callback.inline_message_id,
                                                reply_markup=add_markup(item_id, count, get_korzina()))
            await callback.answer()
    else:
        await callback.answer(f'Количество {count}')


@dp.callback_query_handler(text='back_to_inline')
async def back(callback: types.CallbackQuery):
    await callback.message.delete()
    update_count(callback.from_user.id)
    await callback.answer()
