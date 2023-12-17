from aiogram.dispatcher.filters.state import State, StatesGroup


class Item(StatesGroup):
    kategory = State()
    name = State()
    info = State()
    price = State()
    count = State()
    photo = State()
    photo_url = State()
