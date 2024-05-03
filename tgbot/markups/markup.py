from telebot import types
from tgbot.filters.admin_filter import get_currency


TEXT_BUTTONS_RUS = {
    'take_errors': 'Настройка уведомлений об ошибках сервера',
    'cryptocurrency': 'Настройка отслеживания курса криптовалюты',
}


class BuildMarkup:

    def __init__(self, code='ru'):
        if code == 'ru':
            self.text_btn = TEXT_BUTTONS_RUS

    def get_text(self, key):
        return self.text_btn.get(key)

    def get_button(self, key):
        return types.KeyboardButton(self.text_btn[key])

    def get_inline_button(self, key, callback_data=None, pay=None):
        return types.InlineKeyboardButton(self.text_btn[key],
                                          callback_data=callback_data)

    def main_menu(self):
        markup = types.ReplyKeyboardMarkup(row_width=1,
                                           resize_keyboard=True)
        return markup.add(
            self.get_button('take_errors'),
            self.get_button('cryptocurrency'),
        )

    def main_menu_2(self, data):
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, value in data.items():
            markup.add(
                types.InlineKeyboardButton(
                    f'{value}',
                    callback_data=get_currency.new(currency=value,
                                                   status=True))
            )
        return markup

    def main_menu_3(self, data):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(
                'Перестать отслеживать',
                callback_data=get_currency.new(currency=data,
                                               status=False)))
        return markup
