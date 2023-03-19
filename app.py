from config import TOKEN, exchange_rates
from exceptions import CryptoConverter, APIException
import telebot


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    greetings = 'Этот бот показывает актуальный курс валют. ' \
                '\n ' \
                '\nДля начала работы, введите 3 значения (через пробел): ' \
                '\n1) Количество валюты, которую вы хотите перевести; ' \
                '\n2) Название валюты, количество которой ввели; ' \
                '\n3) Название валюты, в которой Вы хотите узнать цену первой валюты ' \
                '\n ' \
                '\nНапример: 1.5 евро рубль (сколько будет 1.5 евро в рублях)' \
                '\n ' \
                '\nСписок доступных валют: /values '

    bot.reply_to(message, greetings)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in exchange_rates.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        quantity = message.text.split(' ')

        if len(quantity) != 3:
            raise APIException('Введите три параметра')

        amount, quote, base = quantity
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} = {total_base} {base}' \
               '\n' \
               '\n доступные валюты: /values' \
               '\n справка: /help'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
