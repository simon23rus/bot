# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

from states import *

from telegram.ext import Job

WORKING = 1

import telegram_config


def start(bot, update, user_data):
    user_data[u'graph'] = Graph(update.message.from_user.id)
    update.message.text = u'start'
    return work(bot, update, user_data)


def create_keyboard(keys):
    return keys
    # keyboard = []
    # for ind in range(len(keys) // 2):
    #     keyboard.append([keys[2 * ind], keys[2 * ind + 1]])
    # if len(keys) % 2 == 1:
    #     keyboard.append([keys[-1]])
    # return keyboard


def work(bot, update, user_data):
    text = update.message.text
    while True:
        print(u'-0')
        message, keys = user_data[u'graph'].go(text)
        print(u'-1')
        if len(keys) == 0:
            print(u'-2')
            if message:
                print(u'-3, message = "', message, u'"')
                update.message.reply_text(message)
                print(u'-4')
                # bot.sendMessage(update.message.from_user.id, message)
            text = u''
        else:
            keyboard = create_keyboard(keys)
            markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text(message,
                                      reply_markup=markup)
            break
    print(u'-end_while()')

    return WORKING


def error(bot, update, error):
    print(u'OOPS: ', error)
    # logger.warn('Update "%s" caused error "%s"' % (update, error))


def done(bot, update, user_data):
    return ConversationHandler.END


def main():
    updater = Updater(token=telegram_config.bot_token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(u'start', start, pass_user_data=True)],
        states={
            WORKING: [RegexHandler(u'(?!Done)', work, pass_user_data=True)]
        },
        fallbacks=[RegexHandler(u'^Done$', done)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == u'__main__':
    main()
