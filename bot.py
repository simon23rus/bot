

from handlers import *

# def start(bot, update):
#     bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)





def get_user_id(update):
	return  update.message.from_user.id


def main():

	config = open('config', 'r+')
	token = config.readline().split('=')[1][:-1]
	config.close()
	bot = telegram.Bot(token=token)
	updater = Updater(token=token)



	# Create the Updater and pass it your bot's token.

	updater.dispatcher.add_handler(CommandHandler('start', start))
	# updater.dispatcher.add_handler(CallbackQueryHandler(button))
	updater.dispatcher.add_handler(CommandHandler('help', help))
	updater.dispatcher.add_handler(CommandHandler('menu', menu))
	updater.dispatcher.add_error_handler(error)




	# Start the Bot
	updater.start_polling()

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()






	# updates = bot.getUpdates()

	# message = input('Print your mess: ')

	# bot.sendMessage(get_user_id(updates[-1]), message)
	

# /command [optional] [argument]




if __name__ == '__main__':
	main()
