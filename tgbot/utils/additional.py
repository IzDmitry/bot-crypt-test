import json
from tgbot.utils.database import Database
from tgbot.markups.markup import BuildMarkup
from requests import Session

markup = BuildMarkup()
db = Database()


def function_1():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'convert': 'USD'
    }
    headers = {
      'Accepts': 'application/json',
      # Ключ должен быть в env
      'X-CMC_PRO_API_KEY': '96b59f23-1a68-46d2-81aa-342179dc396b',
    }

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        cryptocurrencies = data['data']
        for currency in cryptocurrencies:
            name = currency['name']
            price = currency['quote']['USD']['price']
            db.add_currency(name, price)
    except Exception as e:
        print(e)
