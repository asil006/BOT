from aiogram.dispatcher.filters.state import State, StatesGroup


class Oformit(StatesGroup):
    date = State()
    time = State()
    location = State()
    allow_promocod = State()
    promocod = State()

