import telegram
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

def run_graph(bot, update):
    msg = 'start_choosing'
    graph = Graph('init', bot, update)
    while True:
        msg = graph.go(msg)

def bot_init(bot, update):
    create_user(update.message.from_user.id)
    bot.sendMessage(update.message.from_user.id, 'Дратути')
    return 'start choosing'

def bot_inqueue(bot, update):
    wait_start_cook(update.message.from_user.id)
    bot.sendMessage(update.message.from_user.id, 'Мы начали готовить ваш заказ.')
    return 'start cook'

def bot_start_cook(bot, update):
    wait_end_cook(update.message.from_user.id)
    bot.sendMessage(update.message.from_user.id, 'Ваш заказ готов.')
    wait_for_alarm(update.message.from_user.id)
    return 'end cook'

def bot_alarm(time, bot, update):
    def alarm(bot, update):
        status = wait_end_order(update.message.from_user.id, time)
        bot.sendMessage(update.message.from_user.id, 'Ваш заказ был приготовлен ' + str(time) +  ' минут назад.')
        if status == True:
            return 'end order'
        else:
            return 'save order'
    return alarm

def bot_end_order(bot, update):
    bot.sendMessage(update.message.from_user.id, 'Спасибо за ваш заказ!')
    return 'return'

def bot_blacklist(bot, update):
    return 'lost order'

def bot_banned(bot, update):
    return 'unbanned'

