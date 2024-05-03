import asyncio

# filters
from tgbot.filters.admin_filter import AdminFilter, ParsePrefix, \
    get_currency


# list of storages, you can use any storage
from telebot.asyncio_storage import StateMemoryStorage


# handlers
from tgbot.handlers.admin import admin_user
from tgbot.handlers.spam_command import anti_spam
from tgbot.handlers.user import any_user, any_user_2, any_user_3, any_user_4

# middlewares
from tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware

# states
from tgbot.states.register_state import Currency

# telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import TextMatchFilter, StateFilter


# config
from tgbot import config

from tgbot.utils.additional import function_1, markup, db


bot = AsyncTeleBot(config.TOKEN, state_storage=StateMemoryStorage())


def register_handlers():
    bot.register_message_handler(admin_user, commands=['start'],
                                 admin=True, pass_bot=True)
    bot.register_message_handler(any_user, commands=['start'],
                                 admin=False, pass_bot=True)
    bot.register_message_handler(anti_spam, commands=['spam'], pass_bot=True)

    bot.register_message_handler(any_user_2,
                                 text=[markup.get_text('cryptocurrency')],
                                 pass_bot=True)

    bot.register_callback_query_handler(any_user_3,
                                        parse_prefix=get_currency.filter(),
                                        func=None, pass_bot=True)

    bot.register_message_handler(any_user_4,
                                 state=Currency.value, pass_bot=True)


register_handlers()

# Middlewares
bot.setup_middleware(AntiFloodMiddleware(limit=2, bot=bot))


# custom filters
bot.add_custom_filter(AdminFilter())
bot.add_custom_filter(TextMatchFilter())
bot.add_custom_filter(ParsePrefix())
bot.add_custom_filter(StateFilter(bot))


async def run():
    await bot.polling(non_stop=True, timeout=128)


async def my_task():
    while True:
        # Эта таска должна быть отдельным сервисом
        #function_1()
        for key, value in db.track_currency().items():
            await bot.send_message(key, value)
        await asyncio.sleep(300)


async def main():
    task1 = asyncio.create_task(run())
    task2 = asyncio.create_task(my_task())

    await asyncio.gather(task1, task2)

asyncio.run(main())
