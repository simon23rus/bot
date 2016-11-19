import telegram
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from states import Graph, Node

graph = Graph('init')

def start(bot, update):
    #create_user(update.message.from_user.id)

    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


    # graph.go('start choosing')


def menu(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def choose(bot, update):
    keyboard = [[KeyboardButton('Шаурма'), KeyboardButton('Other Staff')]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=False)

    update.message.reply_text('Please choose product:', reply_markup=reply_markup)

    # graph.go('verify order')

def confirm(bot, update):
    

def button(bot, update):
    query = update.callback_query
    print(query.data)
    if query.data == '1':
        new_keyboard = [[InlineKeyboardButton("novaya", callback_data='1'),
                     InlineKeyboardButton("Option 2", callback_data='2')],

                    [InlineKeyboardButton("Option 3", callback_data='3')]]
        new_reply_markup = InlineKeyboardMarkup(new_keyboard, one_time_keyboard=True, resize_keyboard=True)
       
        bot.editMessageText(text='Please pliz',
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

