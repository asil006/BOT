from aiogram.dispatcher.filters.state import State, StatesGroup


class History(StatesGroup):
    time_admin = State()

    time = State
