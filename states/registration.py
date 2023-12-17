from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    start = State()
    name = State()
    number = State()
