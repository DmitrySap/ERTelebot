import telebot
from exceptions import APIException, CryptoConverter
from config import TOKEN, exchange_rates

bot = telebot.TeleBot(TOKEN)  # создали объект bot, в аргумент передали токен.


@bot.message_handler(commands=['start', 'help'])  # обработчик сообщений (функция вызывается командами start и help)
def start(command):
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

    bot.reply_to(command, greetings)  # бот ответит (метод reply_to) на команду (start / help) приветствием (greetings)


@bot.message_handler(commands=['values'])  # обработчик сообщений (команда values)
def values(command):
    text = 'Доступные валюты:'
    for ticker in exchange_rates.keys():  # для каждого ключа (доллар/евро/рубль) в словаре exchange_rates
        text += '\n' + ticker  # добавь
    bot.reply_to(command, text)  # бот ответит (метод reply_to) на команду (values) текстом (со списком доступных валют)


@bot.message_handler(content_types=['text'])  # обработчик сообщений пользователя (тип контента - текст)
def get_price(message):
    try:
        quantity = message.text.split(' ')  # запрос = текст (написал пользователь), разделенный пробелом
        amount, quote, base = quantity  # запрос состоит из количества, и двух валют (что во что конвертировать)
        total_base = CryptoConverter.get_price(base, quote, amount)  # ответ пользователю (наверно)
        if len(quantity) != 3:  # если запрос состоит не из трех элементов
            raise APIException('Введите три параметра')  # подними ошибку пользователя
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base}: {total_base} {base}'  # текст сообщения
        bot.send_message(message.chat.id, text)  # бот отправит сообщение пользователю текстом


bot.polling(none_stop=True)  # метод polling запускает бота. Noamountne-stop - не прекращать работу
