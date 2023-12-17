from aiogram import types

from loader import dp


@dp.message_handler(state='*')
async def echo(message: types.Message):
    await message.answer(message.text)
