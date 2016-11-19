import telegram
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from requests_to_parse import *

def bot_init(bot, update, order):
    create_user(update.message.from_user.id)
    bot.sendMessage(update.message.from_user.id, 'Дратути')
    return 'start choosing'

def bot_inqueue(bot, update, order):
    wait_start_cook(update.message.from_user.id, order)
    bot.sendMessage(update.message.from_user.id, 'Мы начали готовить ваш заказ.')
    return 'start cook'

def bot_start_cook(bot, update, order):
    wait_end_cook(update.message.from_user.id, order)
    bot.sendMessage(update.message.from_user.id, 'Ваш заказ готов.')
    wait_for_alarm(update.message.from_user.id)
    return 'end cook'

def bot_alarm(time, bot, update, order):
    def alarm(bot, update, order):
        status = wait_end_order(update.message.from_user.id, time, order)
        bot.sendMessage(update.message.from_user.id, 'Ваш заказ был приготовлен ' + str(time) +  ' минут назад.')
        if status == True:
            return 'end order'
        return 'save order'
    return alarm

def bot_end_order(bot, update, order):
    bot.sendMessage(update.message.from_user.id, 'Спасибо за ваш заказ!')
    return 'return'

def bot_blacklist(time, bot, update, order):
    def blacklist(bot, update, order):
        status = wait_end_order(update.message.from_user.id, time, order)
        if status == True:
            return 'end order'
        bot.sendMessage(update.message.from_user.id, 'Вы не забрали ваш заказ (')
        return 'lost order'
    return blacklist

def bot_banned(bot, update, order):
    return 'unbanned'

