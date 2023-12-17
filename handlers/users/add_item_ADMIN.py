from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import ADMINS
from loader import dp
from markups.defaultkeyboard.menu_markup import menu_markup_def_admin, menu_markup_def
from query_data.config import insert_item, get_kategory
from states.add_item import Item


@dp.message_handler(text='➕ Добавить товар[ADMIN]')
async def add_item(message: types.Message):
    await message.delete()
    kategory_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    for i in get_kategory():
        button = KeyboardButton(text=i)
        kategory_markup.insert(button)
    button_back = KeyboardButton(text='🔚 Главный меню')
    kategory_markup.add(button_back)
    await message.answer("Выберите категорию для продукта или напишите сами", reply_markup=kategory_markup)
    await Item.kategory.set()


@dp.message_handler(text="🔚 Главный меню", state=Item.kategory)
async def back_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.delete()
    if str(message.from_user.id) in ADMINS:
        await message.answer('Главный меню', reply_markup=menu_markup_def_admin)
    else:
        await message.answer('Главный меню', reply_markup=menu_markup_def)


@dp.message_handler(state=Item.kategory)
async def kategory_def(message: types.Message, state: FSMContext):
    kategory = message.text
    await state.update_data(
        {"kategory": kategory}
    )
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    await message.answer("Теперь название продукта?", reply_markup=markup)
    await Item.name.set()


@dp.message_handler(text='⬅️ Назад', state=Item.name)
async def back_name(message: types.Message):
    await message.delete()
    kategory_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    for i in get_kategory():
        button = KeyboardButton(text=i)
        kategory_markup.insert(button)
    button_back = KeyboardButton(text='🔚 Главный меню')
    kategory_markup.add(button_back)
    await message.answer("Выберите категорию для продукта или напишите сами", reply_markup=kategory_markup)
    await Item.kategory.set()


@dp.message_handler(state=Item.name)
async def name_def(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {"name": name}
    )
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    await message.answer("Информация о продукте?", reply_markup=markup)
    await Item.info.set()


@dp.message_handler(text='⬅️ Назад', state=Item.info)
async def back_info(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    await message.answer("Отправьте название продукта?", reply_markup=markup)
    await Item.name.set()


@dp.message_handler(state=Item.info)
async def info_def(message: types.Message, state: FSMContext):
    info = message.text
    await state.update_data(
        {"info": info}
    )
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    await message.answer("Цена продукта?", reply_markup=markup)
    await Item.price.set()


@dp.message_handler(text='⬅️ Назад', state=Item.price)
async def back_info(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    await message.answer("Отправьте информация о продукте?", reply_markup=markup)
    await Item.info.set()


@dp.message_handler(state=Item.price)
async def price_def(message: types.Message, state: FSMContext):
    price = message.text
    count = int()
    nums = '1234567890'
    for i in price:
        if i in nums:
            count += 1
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    if len(price) == count:
        await state.update_data({'price': price})
        await message.answer("Количество этого продукта?\n[1-1000]", reply_markup=markup)
        await Item.count.set()
    else:
        await message.answer("Пожалуйста отправьте цену цифрами(1-9)?", reply_markup=markup)


@dp.message_handler(text='⬅️ Назад', state=Item.count)
async def back_info(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    await message.answer("Цена продукта?", reply_markup=markup)
    await Item.price.set()


@dp.message_handler(state=Item.count)
async def count_def(message: types.Message, state: FSMContext):
    count = message.text
    counts = int()
    nums = '1234567890'
    for i in count:
        if i in nums:
            counts += 1
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    if len(count) == counts:
        await state.update_data({'count': count})
        await message.answer("Отправьте фото продукта?", reply_markup=markup)
        await Item.photo.set()
    else:
        await message.answer("Пожалуйста отправьте количеству цифрами(1-9)?", reply_markup=markup)


@dp.message_handler(text='⬅️ Назад', state=Item.photo)
async def back_info(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    await message.answer("Количество этого продукта?\n[1-1000]", reply_markup=markup)
    await Item.count.set()


@dp.message_handler(content_types=['photo'], state=Item.photo)
async def photo_def(message: types.Message, state: FSMContext):
    photo = message.photo[0].file_id
    await state.update_data(
        {'photo': photo})
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    await message.answer('Теперь отправьте ссылку Фото\nСсылку для фото можно получить здесь\nhttps://postimages.org/',
                         reply_markup=markup)
    await Item.next()


@dp.message_handler(state=Item.photo)
async def not_photo(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Назад")
    await message.answer("Пожалуйста отправьте фоту продукта?", reply_markup=markup)


@dp.message_handler(text='⬅️ Назад', state=Item.photo_url)
async def back_photo_url(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⬅️ Назад')
    await message.answer("Отправьте фото продукта?", reply_markup=markup)
    await Item.photo.set()


@dp.message_handler(state=Item.photo_url)
async def photo_url_def(message: types.Message, state: FSMContext):
    photo_url = message.text
    await state.update_data(
        {'photo_url': photo_url})
    async with state.proxy() as data:
        kategory = data['kategory']
        name = data['name']
        info = data['info']
        price = data['price']
        count = data['count']
        await message.answer("Товар успешно был добавлен")
        insert_item(kategory, name, info, price, count, photo_url)
        await message.bot.send_photo(chat_id=message.from_user.id,
                                     photo=f'{photo_url}',
                                     caption=f'{kategory}\nНазвание товара {name}\nИнформация {info}\nСтоимость {price}\nКоличество товара {count}',
                                     reply_markup=menu_markup_def_admin)
    await state.finish()
