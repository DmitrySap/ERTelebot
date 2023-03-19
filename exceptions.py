from config import exchange_rates
import requests
import json


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException('Введите разные валюты.')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты {quote}'
                               '\nКоличество первой валюты должно быть указано: '
                               '\n  целым числом,'
                               '\n или'
                               '\n  дробным числом с разделителем - точкой')
        if float(amount) > 100000000000000:
            raise APIException('Бот не обрабатывает 15-ти (и более) значные суммы')
        if float(amount) <= 0:
            raise APIException('Введите положительное количество валюты')
        try:
            base_ticker = exchange_rates[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            quote_ticker = exchange_rates[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[exchange_rates[base.lower()]]
        return round(total_base * amount, 2)
