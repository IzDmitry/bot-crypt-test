from telebot.asyncio_filters import SimpleCustomFilter, AdvancedCustomFilter
from tgbot.models.users_model import Admin
from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter


get_currency = CallbackData('currency', 'status', prefix='get_currency')


class ParsePrefix(AdvancedCustomFilter):
    key = 'parse_prefix'

    async def check(self, call: types.CallbackQuery,
                    config: CallbackDataFilter):
        return config.check(query=call)


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """
    key = 'admin'

    async def check(self, message):
        return int(message.chat.id) == int(Admin.ADMIN.value)
