from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from markups.defaultkeyboard.number_request import contact_markup
from markups.defaultkeyboard.setting_markup import markup
from query_data.config import change_name, change_number
from query_data.config import get_info_user
from states.setting import Name, Number


@dp.message_handler(text='⚙️ Настройки')
async def top_products(message: types.Message):
    await message.delete()
    info = get_info_user(message.from_user.id)
    await message.answer(f"<b><i>{info[1]} | {info[2]}</i></b>", reply_markup=markup)


@dp.message_handler(text='🔄 Изменить имю')
async def change_name_handler(message: types.Message):
    await message.answer('Отправьте новую имю')
    await Name.name.set()


@dp.message_handler(state=Name.name)
async def name_state(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {'name': name})
    change_name(name, message.from_user.id)
    await message.answer(f'Имя изменено на {name}.', reply_markup=markup)
    await state.finish()


@dp.message_handler(text='🔄 Изменить номер')
async def change_number_handler(message: types.Message):
    await message.answer('Отправьте новый номер или напишите сам.', reply_markup=contact_markup)
    await Number.number.set()


@dp.message_handler(state=Number.number, content_types='contact')
async def name_state(message: types.Message, state: FSMContext):
    number = message.contact.phone_number
    await state.update_data(
        {'number': number})
    await message.answer(f'Номер изменено на {number}.', reply_markup=markup)
    change_number(number, message.from_user.id)
    await state.finish()


@dp.message_handler(state=Number.number)
async def name_state(message: types.Message, state: FSMContext):
    number = message.text
    await state.update_data(
        {'number': number})
    await message.answer(f'Номер изменено на {number}.', reply_markup=markup)
    change_number(number, message.from_user.id)
    await state.finish()
