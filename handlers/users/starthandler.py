from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.config import ADMINS
from loader import dp, db
from markups.defaultkeyboard.menu_markup import menu_markup_def_admin, menu_markup_def
from markups.defaultkeyboard.start_button import start_markup
from query_data.config import get_user_id, get_id_count, create_count_id, update_count
from states.registration import Registration


@dp.message_handler(CommandStart(), state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    lusers = db.execute('select user_id from leviy', fetchall=True)
    leviy_users = []
    for i in lusers:
        for j in i:
            leviy_users.append(j)
    if message.from_user.id in leviy_users:
        pass
    else:
        sql = f"insert into leviy(user_id, name) values({message.from_user.id}, '{message.from_user.first_name}')"
        db.execute(sql, commit=True)
    print(message.from_user.id)
    if str(message.from_user.id) in ADMINS and str(message.from_user.id) in get_user_id():
        await message.answer(f'Главное меню', reply_markup=menu_markup_def_admin)
    elif str(message.from_user.id) in get_user_id():
        await message.answer(f'Главное меню', reply_markup=menu_markup_def)
    else:
        await message.answer(f'Ассаламу алаикум {message.from_user.first_name}', reply_markup=start_markup)
        await message.answer(f"Чтобы пользоваться ботом нужно зарегистрироваться\nНажмите Регистрация")
        await Registration.start.set()
