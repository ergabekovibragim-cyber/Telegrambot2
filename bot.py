import telebot
from telebot import types
import requests

BOT_TOKEN = '8976035335:AAFJ3troaMISVt30YQPH0TZU8-Xbsq0THuE'
API_KEY = 'def3ef7dc48b3944f0e5c1a8'

bot = telebot.TeleBot(BOT_TOKEN)

def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        rates = data['conversion_rates']
        if target_currency in rates:
            return rates[target_currency]

    return None


@bot.message_handler(commands=['convert'])
def convert_currency(message):
    try:
        parts = message.text.split()

        if len(parts) == 4:
            _, amount, base_currency, target_currency = parts
            amount = float(amount)

        elif len(parts) == 3:
            _, base_currency, target_currency = parts
            amount = 1

        else:
            bot.reply_to(
                message,
                "Используйте:\n/convert 100 USD KZT\nили\n/convert USD KZT"
            )
            return

        exchange_rate = get_exchange_rate(
            base_currency.upper(),
            target_currency.upper()
        )

        if exchange_rate:
            converted_amount = amount * exchange_rate
            bot.reply_to(
                message,
                f'{amount} {base_currency.upper()} = {converted_amount} {target_currency.upper()}'
            )
        else:
            bot.reply_to(
                message,
                'Invalid currency code. Please use valid ISO currency codes.'
            )

    except ValueError:
        bot.reply_to(
            message,
            'Invalid format. Please use: /convert 100 USD KZT'
        )

    except Exception as e:
        bot.reply_to(
            message,
            f'An error occurred: {str(e)}'
        )


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(
        message,
        "Команды бота:\n\n"
        "/convert <сумма> <валюта1> <валюта2>\n"
        "Пример:\n"
        "/convert 100 USD KZT\n\n"
        "Если ввести только валюты:\n"
        "/convert USD KZT\n"
        "будет использована сумма 1."
    )


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("USD KZT")
    btn2 = types.KeyboardButton("KZT USD")
    btn3 = types.KeyboardButton("EUR KZT")
    btn4 = types.KeyboardButton("KZT EUR")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Выберите валюты кнопкой или используйте /convert",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text in [
    "USD KZT",
    "KZT USD",
    "EUR KZT",
    "KZT EUR"
])
def button_convert(message):
    base_currency, target_currency = message.text.split()

    exchange_rate = get_exchange_rate(
        base_currency,
        target_currency
    )

    if exchange_rate:
        bot.reply_to(
            message,
            f"1 {base_currency} = {exchange_rate} {target_currency}"
        )


bot.polling()