import telegram
from telegram.ext import Updater

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def get_user_id(update):
	return  update.message.from_user.id


def main():

	config = open('config', 'r+')
	token = config.readline().split('=')[1][:-1]
	config.close()
	bot = telegram.Bot(token=token)
	updater = Updater(token=token)

	updates = bot.getUpdates()

	message = input('Print your mess: ')

	bot.sendMessage(get_user_id(updates[0]), message)
	





if __name__ == '__main__':
	main()