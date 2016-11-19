import telegram
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from requests_to_parse import *

def bot_init(bot, update, menu):
    create_user(update.message.from_user.id)
    bot.sendMessage(update.message.from_user.id, 'Дратути')
    return 'start choosing'

def bot_inqueue(bot, update, menu):
    wait_start_cook(update.message.from_user.id, menu)
    bot.sendMessage(update.message.from_user.id, 'Мы начали готовить ваш заказ.')
    return 'start cook'

def bot_start_cook(bot, update, menu):
    wait_end_cook(update.message.from_user.id, menu)
    bot.sendMessage(update.message.from_user.id, 'Ваш заказ готов.')
    wait_for_alarm(update.message.from_user.id)
    return 'end cook'

def bot_alarm(time, bot, update, menu):
    def alarm(bot, update, menu):
        status = wait_end_order(update.message.from_user.id, time, menu)
        bot.sendMessage(update.message.from_user.id, 'Ваш заказ был приготовлен ' + str(time) +  ' минут назад.')
        if status == True:
            return 'end order'
        return 'save order'
    return alarm

def bot_end_order(bot, update, menu):
    bot.sendMessage(update.message.from_user.id, 'Спасибо за ваш заказ!')
    return 'return'

def bot_blacklist(time, bot, update, menu):
    def blacklist(bot, update, menu):
        status = wait_end_order(update.message.from_user.id, time, menu)
        if status == True:
            return 'end order'
        bot.sendMessage(update.message.from_user.id, 'Вы не забрали ваш заказ (')
        return 'lost order'
    return blacklist

def bot_banned(bot, update, menu):
    return 'unbanned'

