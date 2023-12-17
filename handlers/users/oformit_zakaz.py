import datetime
import random
import string

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

import markups.defaultkeyboard.location_request
from data.config import ADMINS
from loader import dp, bot, db
from markups.defaultkeyboard.date_markup import date_markup, date_list
from markups.defaultkeyboard.menu_markup import menu_markup_def, menu_markup_def_admin
from query_data.config import my_basket, oformlenie, delete_item, get_oformleniya, minus_count_item, add_promokod, \
    delete_korzina_item, get_promokod, delete_promokod
from states.oformleniye import Oformit


@dp.message_handler(text='📑 Оформить заказ')
async def zakaz_oformit(message: types.Message):
    print(datetime.datetime.now().time().hour)
    await message.delete()
    i = my_basket(str(message.from_user.id))
    s = ''
    money = int()
    for j in i:
        s += f"{j[1]}\n{j[3]}KZT x {j[4]} = {j[3] * j[4]}KZT\n{j[2]}\n\n"
        money += (j[3] * j[4])
    await message.answer(f"{s}Итог - {money}KZT")
    await message.answer(f"Выберите Дату для заказа", reply_markup=date_markup)
    await Oformit.date.set()


@dp.message_handler(text="🔚 Главный меню", state=Oformit.date)
async def back_menu(message: types.Message, state: FSMContext):
    if str(message.from_id) in ADMINS:
        await message.answer("Главный меню", reply_markup=menu_markup_def_admin)
    else:
        await message.answer("Главный меню", reply_markup=menu_markup_def)
    await state.finish()


@dp.message_handler(text=date_list, state=Oformit.date)
async def date_def(message: types.Message, state: FSMContext):
    date = message.text
    await state.update_data(
        {'date': date})
    await message.answer(f"Время доставки", reply_markup=time_markups(date))
    await Oformit.next()


@dp.message_handler(state=Oformit.date)
async def not_date(message: types.Message):
    await message.answer("Пожалуйста выберите дату а не введите сами!!!", reply_markup=date_markup)


time_list = []
for y in range(10, 22):
    time_list.append(str(y + 1) + ':00')


@dp.message_handler(text=time_list, state=Oformit.time)
async def time_def(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data({'time': time})
    await message.answer('Отправьте свою локацию', reply_markup=markups.defaultkeyboard.location_request.location_markup)
    await Oformit.next()


@dp.message_handler(text='⬅️ Назад', state=Oformit.time)
async def back_time(message: types.Message):
    await message.answer(f"Выберите Дату для заказа", reply_markup=date_markup)
    await Oformit.date.set()


@dp.message_handler(state=Oformit.time)
async def not_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        date = data['date']
    await message.answer("Пожалуйста выберите времю а не введите сами!!!", reply_markup=time_markups(date))


@dp.message_handler(state=Oformit.location, content_types='location')
async def location_def(message: types.Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await state.update_data(
        {'latitude': latitude}
    )
    await state.update_data(
        {'longitude': longitude}
    )
    if len(get_promokod(message.from_user.id)) > 0:
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.row('✅ Использовать Промокод', '❌ Не использовать')
        await message.answer('Хотите использовать Промокод?', reply_markup=markup)
        await Oformit.next()
    else:
        if str(message.from_user.id) in ADMINS:
            await message.answer('Ваш заказ одобрен\nВ течение 30 минут вам обратиться наш менеджер',
                                 reply_markup=menu_markup_def_admin)
        else:
            await message.answer('Ваш заказ одобрен\nВ течение 30 минут вам обратиться наш менеджер',
                                 reply_markup=menu_markup_def)
        s = str()
        money = int()
        i = my_basket(str(message.from_user.id))
        delete_item(message.from_user.id)
        for j in i:
            delete_korzina_item(j[0], j[6])
            minus_count_item(j[0], j[4])
            s += f"{j[1]}\n{j[3]}KZT x {j[4]} = {j[3] * j[4]}KZT\n{j[2]}\n\n"
            money += (j[3] * j[4])

        insert_promo(money, message)
        async with state.proxy() as data:
            date = data['date']
            time = data['time']
            oformlenie(time, date, message.from_user.id, money, s, latitude, longitude)
        await send_mess_to_admin(message)
        await state.finish()


@dp.message_handler(text='⬅️ Назад', state=Oformit.location)
async def back_to_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        date = data['date']
    await message.answer(f"Время доставки", reply_markup=time_markups(date))
    await Oformit.time.set()


@dp.message_handler(state=Oformit.location)
async def time_def(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйуста отправьте локацию!')
    await time_def(message, state)


@dp.message_handler(text='✅ Использовать Промокод', state=Oformit.allow_promocod)
async def allow_promocod_def(message: types.Message):
    await message.delete()
    promokod_list = get_promokod(message.from_user.id)
    await message.answer(
        'Отправьте ваш Промокод упоминаю что нельзя отправьлять чужие Промокоды они все равно не будут применены!')
    promocod = str()
    for i in promokod_list:
        promocod += f'<code>{i[0]}</code>\t|'
        promocod += str(f'\t{i[1]}%\n')
    promocod += 'Чтобы скопировать Промокод нажмите на него!'
    await message.answer(promocod)
    await Oformit.next()


@dp.message_handler(text='❌ Не использовать', state=Oformit.allow_promocod)
async def allow_not_promocod_def(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        latitude = data['latitude']
        longitude = data['longitude']
    await message.delete()
    if str(message.from_user.id) in ADMINS:
        await message.answer('Ваш заказ одобрен\nВ течение 30 минут вам обратиться наш менеджер',
                             reply_markup=menu_markup_def_admin)
    else:
        await message.answer('Ваш заказ одобрен\nВ течение 30 минут вам обратиться наш менеджер',
                             reply_markup=menu_markup_def)
    s = str()
    money = int()
    i = my_basket(str(message.from_user.id))
    delete_item(message.from_user.id)
    for j in i:
        delete_korzina_item(j[0], j[6])
        minus_count_item(j[0], j[4])
        s += f"{j[1]}\n{j[3]}KZT x {j[4]} = {j[3] * j[4]}KZT\n{j[2]}\n\n"
        money += (j[3] * j[4])
    insert_promo(money, message)
    async with state.proxy() as data:
        date = data['date']
        time = data['time']
        oformlenie(time, date, message.from_user.id, money, s, latitude, longitude)
    await send_mess_to_admin(message)
    await state.finish()


@dp.message_handler(state=Oformit.promocod)
async def promocod_def(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        latitude = data['latitude']
        longitude = data['longitude']
    promokod_list = get_promokod(message.from_user.id)
    promo = message.text
    promos = []
    for p in promokod_list:
        promos.append(p[0])
    if promo in promos:
        for p in promokod_list:
            if promo == p[0]:
                s = ''
                money = int()
                i = my_basket(str(message.from_user.id))
                delete_item(message.from_user.id)
                delete_promokod(p[0], message.from_user.id)
                for j in i:
                    delete_korzina_item(j[0], j[6])
                    minus_count_item(j[0], j[4])
                    print(j[3], j[4])
                    s += f"{j[1]}\n{j[3]}KZT x {j[4]} = {j[3] * j[4]}KZT - {p[1]}%\n{j[2]}\n\n"
                    money += (j[3] * j[4])
                money = money / 100 * (100 - p[1])
                async with state.proxy() as data:
                    date = data['date']
                    time = data['time']
                    oformlenie(time, date, message.from_user.id, money, s, latitude, longitude)
                insert_promo(money, message)
                if str(message.from_user.id) in ADMINS:
                    await message.answer(
                        'Промокод Успешно использован\nВаш заказ одобрен\nВ течение 30 минут вам обратиться наш менеджер',
                        reply_markup=menu_markup_def_admin)
                else:
                    await message.answer(
                        'Промокод Успешно использован\nВаш заказ одобрен\nВ течение 30 минут вам обратиться наш менеджер',
                        reply_markup=menu_markup_def)
                await state.finish()
                await send_mess_to_admin(message)
                break
    else:
        await message.answer('У вас нету такого Промокода', reply_markup=ReplyKeyboardRemove())
        await Oformit.allow_promocod.set()
        await allow_promocod_def(message)


def insert_promo(pul, message):
    letters = str()
    letters += string.ascii_uppercase
    letters += '1234567890'
    promokod = ''.join(random.choice(letters) for i in range(10))
    if 3000 <= pul <= 5000:
        add_promokod(promokod, message.from_user.id, 5)
    elif 5000 <= pul <= 15000:
        add_promokod(promokod, message.from_user.id, 10)
    elif 15000 <= pul:
        add_promokod(promokod, message.from_user.id, 15)


def time_markups(date):
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    time_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    if date == str(datetime.datetime.now().date()):
        for i in range(10, 22):
            if i > datetime.datetime.now().time().hour:
                button = KeyboardButton(text=str(i + 1) + ':00')
                time_markup.insert(button)
    else:
        for i in range(10, 22):
            button = KeyboardButton(text=str(i + 1) + ':00')
            time_markup.insert(button)
    time_markup.add("⬅️ Назад")
    return time_markup


async def send_mess_to_admin(message):
    item = get_oformleniya()
    user = db.execute(f"select * from registration where user_id = '{message.from_user.id}'", fetchone=True)
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Заказ был одобрен на дату - {item[2]}, {item[1]}\n\n{item[5]}\nИтог - {item[3]}\nАкк - <a href='tg://user?id={item[4]}'>{message.from_user.first_name}</a> @{message.from_user.username}\nНомер {user[2]}",
                           disable_web_page_preview=True)
    await bot.send_location(chat_id=ADMINS[0],
                            latitude=item[6],
                            longitude=item[7],
                            reply_markup=menu_markup_def_admin)
