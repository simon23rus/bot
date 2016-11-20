from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import telegram_config

print(telegram_config.bot_token)

import logging

from states import *

WORKING = 1



def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('%s - %s' % (key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update, user_data):
    print('abcd')
    user_data['graph'] = Graph(bot, update.message.from_user.id)
    update.message.text = 'start'
    return work(bot, update, user_data)


def createKeyboard(keys):
    keyboard = []
    for ind in range(len(keys) // 2):
        print(ind)
        keyboard.append([keys[2 * ind], keys[2 * ind + 1]])
    
    if len(keys) % 2 == 1:
        keyboard.append([keys[-1]])

    return keyboard


def work(bot, update, user_data):
    text = update.message.text
    while True:
        print('while1')
        message, keys = user_data['graph'].go(text)
        print('while2')
        if len(keys) == 0:
            update.message.reply_text(message)
            text = ''
        else: 
            keyboard = createKeyboard(keys)
            markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text(message,
                                    reply_markup=markup)
            break
        
    return WORKING

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def done(bot, update, user_data):
    print('zazaz')
    return ConversationHandler.END

    return '|'.join(ans)
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=telegram_config.bot_token)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],

        states={
            WORKING: [RegexHandler('(?!Done)', work, pass_user_data=True)]
        },

        fallbacks=[RegexHandler('^Done$', done)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()