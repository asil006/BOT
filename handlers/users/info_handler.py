from aiogram import types

from loader import dp
from markups.defaultkeyboard.info_markup import markup
from middlewares.my_location import location


@dp.message_handler(text='ℹ️ Информация')
async def info(message: types.Message):
    await message.delete()
    await message.answer(
        "Этот бот был создан для того чтобы заказать вещи любого вида в том числе:\n"
        "<b>Еда, Спорт, Техника, Мебели</b>\n"
        "И хочу упомянуть что мы работаем только с доставкой а если хотите прийти сам и забрать свой вещь\n"
        "Мы отправим вам локацию\n"
        "Нажмите - <b>📍Локация АР shop</b>", reply_markup=markup)


@dp.message_handler(text='📍Локация АР shop')
async def location_hand(message: types.Message):
    await message.answer_location(location['latitude'], location['longitude'])
