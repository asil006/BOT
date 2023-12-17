from aiogram import types

from loader import dp
from query_data.config import get_promokod


@dp.message_handler(text='📩 Мои промокоды')
async def promocods_handler(message: types.Message):
    await message.delete()
    promocod = str()
    list = get_promokod(message.from_user.id)
    if len(list) == 0:
        await message.answer('У вас пока нет Промокодов!')
    else:
        for i in list:
            promocod += f'<code>{i[0]}</code>\t|'
            promocod += str(f'\t{i[1]}%\n------------------------------\n')
        promocod += 'Чтобы скопировать Промокод нажмите на него!'
        await message.answer(promocod)
