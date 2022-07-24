from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMMailing(StatesGroup):
    text = State()
    apply = State()



