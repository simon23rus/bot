import telegram
from telegram.ext import Updater

token = '290457805:AAEzZlFxuUTwTzJYzhK7UcLoRhKdbkEVers'

bot = telegram.Bot(token=token)
updater = Updater(token=token)

updates = bot.getUpdates()



def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")