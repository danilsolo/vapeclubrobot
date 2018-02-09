#coding:utf-8
import telebot
import sqlite3
import logging
import random
import time
import datetime
from telebot import types


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s'
                    , level = logging.INFO)


def niceprint(string):
    tabindex = 0
    out = ''
    for i in string:
        if i == ',':
            out += i
            out += '\n'
            out += '\t' * tabindex
            continue
        if i == '{':
            tabindex += 1
        if i == '}':
            tabindex -= 1
            out += '\n'
        out += i
    return out

bot = telebot.TeleBot('490087158:AAHoaogoaMRhm4IJdwWs95oPUuvtH3zWdHw')

a = []
keyboard = telebot.types.InlineKeyboardMarkup()

gobutton = telebot.types.InlineKeyboardButton('Иду', callback_data='ok')
negobutton = telebot.types.InlineKeyboardButton('Хуй пойду', callback_data='neok')
keyboard.row(gobutton, negobutton)

letsgobutton = telebot.types.InlineKeyboardButton('Встали вышли', callback_data='letsgo')
keyboard.row(letsgobutton)

adminskeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
adminskeyboard.add(*[telebot.types.KeyboardButton(name) for name in ['го пыхать', 'убрать клаву']])

adminskeyboarhide = telebot.types.ReplyKeyboardRemove()

@bot.callback_query_handler(func=lambda call: call.data == 'ok')
def go(call):
    # bot.send_message(call.message.chat.id, 'Жопа')
    if call.from_user.username in a:
        bot.answer_callback_query(call.id, text='Ты уже идешь блять!')
    else:
        a.append(call.from_user.username)
        print(a)
        out = '''Кто же пойдет заниматься покайфной хуйней на улочку.\n\nУчастники:'''
        for i in a:
            out += '\n' + '- ' + str(i)
        bot.edit_message_text(out, call.message.chat.id, call.message.message_id, reply_markup=keyboard
                              , parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == 'neok')
def nego(call):
    # bot.send_message(call.message.chat.id, 'Жопа')
    bot.answer_callback_query(call.id, text='натурал блять!')


@bot.callback_query_handler(func=lambda call: call.data == 'letsgo')
def chooser(call):
    global a
    if len(a) == 0:
        bot.answer_callback_query(call.id, 'Ну и кто пойдет то бля')
    if len(a) == 1:
        bot.answer_callback_query(call.id, 'Ну и иди один')

    if len(a) > 1:
        logging.info(a)
        random.shuffle(a)
        logging.info(a)
        out = '''Кто же будет первым пидором".\n\nУчастники:'''
        for indx, i in enumerate(a):
            out += '\n' + str(indx + 1) + '. @' + str(i)

        out += '\n\nПервый пидор: ' + '@' + a[0]
        out += '\n\nА теперь пиздуйте'
        a = []
        bot.edit_message_text(out, call.message.chat.id, call.message.message_id
                              , parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    userid = message.from_user.id
    username = message.from_user.username

    logging.info('user: ' + str(username) + ' command: /start')
    bot.send_message(message.chat.id, 'Привет пидоры', reply_markup=adminskeyboard)


@bot.message_handler(func=lambda message: message.text and 'го пыхать' in message.text, content_types=['text'])
def go(message):
    logging.info('user: ' + str(message.from_user.username) + ' позвал')
    msg = bot.send_message(message.chat.id, 'Кто же пойдет заниматься покайфной хуйней на улочку', reply_markup=keyboard)
    bot.pin_chat_message(msg.chat.id, msg.message_id)

@bot.message_handler(func=lambda message: message.text and 'убрать клаву' in message.text, content_types=['text'])
def go(message):
    logging.info('user: ' + str(message.from_user.username) + ' убрал клаву')
    bot.send_message(message.chat.id, 'Ой все', reply_markup=adminskeyboarhide)

bot.polling()