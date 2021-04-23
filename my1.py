#мой первый бот!

import telebot
from telebot import types

#1756417710:AAG6UG4p8lOfxqw4svTL8pWmShN4YgLUDkc

name = ""
surname = ""
age = 0

bot = telebot.TeleBot("1756417710:AAG6UG4p8lOfxqw4svTL8pWmShN4YgLUDkc")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! получи подарок за регистрацию, нажми -> /reg!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'привет':
        bot.reply_to(message, 'Привет создатель бота!' )
    elif message.text == 'подарок':
        bot.reply_to(message, 'шутка!')
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, reg_name)

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "а фамилия?")
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "твой возраст?")
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    if age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Водите число цифрами!")

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет? И тебя зовут: ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Спасибо за регистрацию, подарок ждет вас!')
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'давай по новой!')
        bot.send_message(call.message.chat.id, "Привет, как тебя зовут?")
        bot.register_next_step_handler(call.message, reg_name)
bot.polling()
