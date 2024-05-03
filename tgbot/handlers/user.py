from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from tgbot.utils.additional import markup, db, function_1
from tgbot.filters.admin_filter import get_currency
from tgbot.states.register_state import Currency


async def any_user(message: Message, bot: AsyncTeleBot):
    """
    You can create a function and use parameter pass_bot.

    """

    try:
        function_1()
        text = 'Выберите действие'
        await bot.send_message(message.chat.id, text,
                               reply_markup=markup.main_menu())
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


async def any_user_2(message: Message, bot: AsyncTeleBot):
    try:
        currency = db.get_currency()
        text = 'Выберите валюту'
        await bot.send_message(message.chat.id, text,
                               reply_markup=markup.main_menu_2(currency))
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


async def any_user_3(call: CallbackQuery, bot: AsyncTeleBot):
    call_data: dict = get_currency.parse(callback_data=call.data)

    try:
        get_data = db.get_track_currency(call.message.chat.id,
                                         call_data['currency'])
        if not get_data:
            text = 'Введите пароговые значения в формате min/max'
            await bot.set_state(call.message.chat.id,
                                Currency.value, call.message.chat.id)
            await bot.delete_message(call.message.chat.id,
                                     call.message.message_id)
            await bot.send_message(call.message.chat.id, text)
            async with bot.retrieve_data(call.message.chat.id,
                                         call.message.chat.id) as data:
                data['currency'] = call_data['currency']
                data['status'] = call_data['status']
        else:
            if call_data['status'] == 'True':
                text = f'Валюта:{get_data[0]} \
                         \nМакс:{get_data[1]}\nМин:{get_data[2]}'
                await bot.edit_message_text(
                    text, call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup.main_menu_3(get_data[0]))

            else:
                await bot.delete_message(call.message.chat.id,
                                         call.message.message_id)
                db.del_track_currency(call.message.chat.id, get_data[0])
                await bot.send_message(call.message.chat.id, 'Удалено')
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


async def any_user_4(message: Message, bot: AsyncTeleBot):
    async with bot.retrieve_data(message.from_user.id,
                                 message.chat.id) as data:
        numbers = message.text.split('/')
        try:
            if isinstance(float(numbers[0]),
                          float) and isinstance(float(numbers[1]), float):
                db.add_track_currency(message.chat.id,
                                      data['currency'],
                                      float(numbers[1]),
                                      float(numbers[0]))
                await bot.send_message(message.chat.id, 'Валюта отслеживается')
        except Exception as e:
            print(e)
            await bot.send_message(message.chat.id, 'Вне диапазона')
    await bot.delete_state(message.from_user.id, message.chat.id)
