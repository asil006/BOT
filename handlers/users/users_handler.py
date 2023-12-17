from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
from loader import dp
from markups.defaultkeyboard.number_request import contact_markup
from query_data.config import insert_user
from states.registration import Registration
from markups.defaultkeyboard.start_button import start_markup
from markups.defaultkeyboard.menu_markup import menu_markup_def, menu_markup_def_admin


@dp.message_handler(text='Регистрация', state=Registration.start)
async def registration(message: types.Message):
    await message.answer(f"Введите вашу имю для регистрации", reply_markup=ReplyKeyboardRemove())
    await Registration.name.set()


@dp.message_handler(state=Registration.start)
async def not_registration(message: types.Message):
    await message.answer(f"Пожалуйста нажмите Регистрация❗️", reply_markup=start_markup)
    await Registration.start.set()


@dp.message_handler(state=Registration.name)
async def name_state(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {'name': name})
    await message.answer(f'{name} тепер отправьте ваш номер', reply_markup=contact_markup)
    await Registration.number.set()


@dp.message_handler(content_types='contact', state=Registration.number, is_sender_contact=True)
async def phone_number(message: types.Message, state: FSMContext):
    number = message.contact.phone_number
    await state.update_data(
        {'number': number}
    )
    await message.answer('✅ Успешно')
    async with state.proxy() as data:
        name = data['name']
        number = data['number']
        insert_user(name, number, message.from_user.id)
    if str(message.from_user.id) in ADMINS:
        await message.answer("Теперь выбирайте нужную себе категорию", reply_markup=menu_markup_def_admin)
    else:
        await message.answer("Теперь выбирайте нужную себе категорию", reply_markup=menu_markup_def)

    await state.finish()


@dp.message_handler(state=Registration.number)
async def phone_number(message: types.Message):
    await message.answer('Пожалуйста отправьте свой контакт нажимая кнопку contact❗️', reply_markup=contact_markup)


@dp.message_handler(text='🔚 Главный меню')
async def glavniy_menu(message: types.Message):
    await message.delete()
    if str(message.from_user.id) in ADMINS:
        await message.answer('Главный меню', reply_markup=menu_markup_def_admin)
    else:
        await message.answer('Главный меню', reply_markup=menu_markup_def)
