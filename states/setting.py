from aiogram.dispatcher.filters.state import State, StatesGroup


class Name(StatesGroup):
    name = State()


class Number(StatesGroup):
    number = State()
