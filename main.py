from aiogram import executor

import handlers
import filters
import middlewares
import utils.misc.logging
from loader import dp
from query_data.config import create_tables
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    create_tables()
    await on_startup_notify(dispatcher)

    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=on_startup)
