from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp
from markups.defaultkeyboard.menu_markup import menu_markup_def_admin, menu_markup_def
from query_data.config import db, get_user_id, get_kategory


def items(kategory):
    list_item = []
    try:
        fetchall = db.execute(f"""select * from item where kategory = '{kategory}'""", fetchall=True)
        for i in fetchall:
            list_item.append(i)
        return list_item
    except Exception as err:
        print(err)


@dp.inline_handler(text=get_kategory())
async def inline(inline: types.InlineQuery):
    msg = []
    for i in items(inline.query):
        msg.append((
            types.InlineQueryResultArticle(
                id=str(i[0]),
                title=i[2],
                input_message_content=types.InputMessageContent(
                    message_text=i[2]
                ),
                thumb_url=i[6],
                description=i[3]
            )

        ))
    msg.append((
        types.InlineQueryResultArticle(
            id=str('back'),
            title='⬅️ Назад',
            input_message_content=types.InputMessageContent(
                message_text="⬅️ Назад в категорию"
            ),
            thumb_url='https://cdn.pixabay.com/photo/2017/06/20/14/55/icon-2423347_1280.png',
            description="Возвращает назад в категорию"

        )

    ))
    await inline.answer(results=msg)


@dp.message_handler(text='⬅️ Назад в категорию')
async def nazad(message: types.Message):
    await message.delete()


@dp.callback_query_handler(text='back_to_menu')
async def back(callback: types.CallbackQuery):
    await callback.message.delete()
    if str(callback.from_user.id) in ADMINS:
        await callback.message.answer(f'Главный меню', reply_markup=menu_markup_def_admin)
    elif str(callback.from_user.id) in get_user_id():
        await callback.message.answer(f'Главный меню {callback.from_user.first_name}', reply_markup=menu_markup_def)
    await callback.answer()
