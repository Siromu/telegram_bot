import telebot
from tok import token, crypts
from extensions import CryptoConvertor, ConvertionException

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['hi'])
def hi_user(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Приветики, {message.chat.first_name}")


@bot.message_handler(commands=['start', 'help'])
def bot_help(message: telebot.types.Message):
    text = f'{message.chat.first_name}, отправьте сообщение боту в виде: \n' \
    f'<имя валюты, цену которой Вы хотите узнать> <имя валюты, цену в которой надо узнать> ' \
    f'<количество переводимой валюты>. \n' \
    f'Команда "/values" выводит информацию о всех доступных валютах; \n' \
    f'При вводе команды "/hi" бот радостно поприветствует Вас :) '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in crypts.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        price = CryptoConvertor.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base}: {price}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True, interval=0)

