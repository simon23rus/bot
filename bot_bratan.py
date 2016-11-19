import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, CONFIRMATION, TYPING_CHOICE = range(3)

product_keyboard = [['Шаверма'],['Other Staff'], ['Exit']]

confirmation_keyboard = [['Да'], ['Нет']]

product_markup = ReplyKeyboardMarkup(product_keyboard, one_time_keyboard=True)
confirmation_markup = ReplyKeyboardMarkup(confirmation_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('%s - %s' % (key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    update.message.reply_text('Здравствуйте, у Вас есть выбор одной из _двух_ основных частей нашей кухни." " Что выберете Вы?',
        reply_markup=product_markup)

    return CHOOSING


def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    # update.message.reply_text('Your %s? Yes, I would love to hear about that!' % text.lower())

    return CONFIRMATION




def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "%s"
                              "You can tell me more, or change your opinion on something."
                              % facts_to_str(user_data),
                              reply_markup=confirmation_markup)

    return CHOOSING


def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "%s"
                              "Until next time!" % facts_to_str(user_data))

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
	# Create the Updater and pass it your bot's token.
	config = open('config', 'r+')
	token = config.readline().split('=')[1][:-1]
	config.close()
	bot = telegram.Bot(token=token)
	updater = Updater(token=token)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
	conv_handler = ConversationHandler(
	    entry_points=[CommandHandler('start', start)],

	    states={
	        CHOOSING: [RegexHandler('^(Шаверма|Other Staff)$',
	                                regular_choice,
	                                pass_user_data=True),
	                  ],

	        CONFIRMATION: [MessageHandler(Filters.text,
	                                      received_information,
	                                      pass_user_data=True),
	                       ],
	    },

	    fallbacks=[RegexHandler('^Exit$', done, pass_user_data=True)]
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