import telegram
import logging
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup)

from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, RegexHandler, Filters)

# from states import Graph, Node
from process_orders import *

def start(bot, update):
    #create_user(update.message.from_user.id)
    # run_graph(bot, update)
    print("ZDAROVA, BRATAN")

    bot_choose(bot, update)


    bot_make_order(bot, update)
   

def bot_choose(bot, update):
    keyboard = [[InlineKeyboardButton('Шаурма', callback_data='1'), InlineKeyboardButton('Other Staff', callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    bot.sendMessage(chat_id = update.message.chat_id, text='Что Вы хотите заказать', reply_markup=reply_markup)



def bot_make_order(bot, update):
    keyboard = [[InlineKeyboardButton('Да', callback_data='10'), InlineKeyboardButton('Нет',callback_data='11')]]

    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    bot.sendMessage(chat_id = update.message.chat_id, text='Готовы ли Вы подтвердить Ваш заказ?', reply_markup=reply_markup)

def menu(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def button(bot, update):
    query = update.callback_query
    print(query.data)
    if query.data == '1':
        new_keyboard = [[InlineKeyboardButton("Да", callback_data='1'),
                     InlineKeyboardButton("Нет", callback_data='2')]]
        new_reply_markup = InlineKeyboardMarkup(new_keyboard, one_time_keyboard=True, resize_keyboard=True)
       
        bot.editMessageText(text='Готовы подтвердить заказ?',
                chat_id=query.message.chat_id,
                message_id=query.message.message_id)

        # update.message.reply_text('New choosing:', reply_markup=new_reply_markup)

        bot.editMessageReplyMarkup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=new_reply_markup)
        # bot.editMessageText(text="U lalka : %s" % query.data,
        #         chat_id=query.message.chat_id,
        #         message_id=query.message.message_id)

    else:
        bot.editMessageText(text="Selected option: %s" % query.data,
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id)

def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))

