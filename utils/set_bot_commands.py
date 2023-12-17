from aiogram import Dispatcher, types


async def set_default_commands(disp: Dispatcher):
    await disp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("info", "Информация о боте")
    ])
