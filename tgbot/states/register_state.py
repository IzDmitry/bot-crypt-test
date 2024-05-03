from telebot.asyncio_handler_backends import State, StatesGroup


class Currency(StatesGroup):
    """
    Group of states for registering
    """
    value = State()
