from aiogram import types

from loader import dp


@dp.message_handler(text="☎️ Обратная связь")
async def aloqa(message: types.Message):
    await message.delete()
    await message.answer(f'<a href="tg://user?id=1529211373">Admin</a> | '
                         "<a href= 'https://instagram.com/asanov_dir'>Instagram</a> | "
                         "<a href= 'asilbekxasanov06@gmail.com'>Email</a>")
