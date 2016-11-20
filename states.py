from handlers import *
from parse_utils import *
from process_orders import *

import telegram
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from requests_to_parse import *

class Node:
    def __init__(self, name, feedback):
        self.map = {}
        self.name = name
        self.feedback = feedback

    def add_adj(self, message, node):
        self.map[message] = node

    def go(self, message):
        return self.map.get(message, self.map.get(''))

class MenuData:
    def __init__(self, menu):
        self.menu = menu
        self.order = None
        self.item = None

class Graph:
    def __init__(self, bot, userId, alarm_time = [5,10,15]):
        init_parse()
        menu = Menu()
        self.nodes = {}
        self.bot = bot
        self.menu_data = MenuData(menu)
        self.userId = userId
        self.cur_node = self.nodes['init']

        init = self.add_node('init', self.bot_init)
        choose = self.add_node('choose', self.bot_choose)
        make_order = self.add_node('make_order', self.bot_make_order)
        inqueue = self.add_node('inqueue', self.bot_inqueue)
        start_cook = self.add_node('start_cook', self.bot_start_cook)
        end_cook = self.add_node('end_cook', self.bot_end_cook)
        alarm1 = self.add_node('alarm1', self.bot_alarm(alarm_time[0]))
        alarm2 = self.add_node('alarm2', self.bot_alarm(alarm_time[1]))
        blacklist = self.add_node('blacklist', self.bot_blacklist(alarm_time[2]))
        banned = self.add_node('banned', self.bot_banned)
        end_order = self.add_node('end_order', self.bot_end_order)

        self.add_edge(init, choose, 'start choosing')
        self.add_edge(choose, make_order, 'verify order')
        self.add_edge(make_order, choose, 'return')
        self.add_edge(make_order, inqueue, 'wait inqueue')
        self.add_edge(inqueue, start_cook, 'start cook')
        self.add_edge(start_cook, end_cook, 'end cook')
        self.add_edge(end_cook, alarm1, 'save order')
        self.add_edge(alarm1, end_order, 'end order')
        self.add_edge(alarm2, end_order, 'end order')
        self.add_edge(end_cook, alarm1, 'wait getting')
        self.add_edge(alarm1, alarm2, 'save order')
        self.add_edge(alarm2, blacklist, 'save order')
        self.add_edge(blacklist, banned, 'ban')
        self.add_edge(blacklist, choose, 'lost order')
        self.add_edge(banned, choose, 'unbanned')
        self.add_edge(end_order, choose, 'return')

        return self

    def add_node(self, name):
        node = Node(name)
        self.nodes[name] = node
        return node

    def add_edge(self, src, dst, message):
        src.add_adj(message, dst)

    def bot_init(text):
        create_user(self.userId)
        bot.sendMessage(self.userId, 'Дратути')
        message = 'Выберите продукт:'
        keys = self.menu_data.menu.get_item_names()
        return 'start choosing', message, keys

    def bot_choose(text):
        self.menu_data.item = text
        message = 'Ваш заказ: ' + text + ', готовы ли Вы подтвердить?'
        keys = ['Да', 'Нет']
        return 'verify order', message, keys

    def bot_make_order(text):
        menu_data.order = menu.place_order_by_name(update.message.from_user.id, menu_data.item)
        message = 'Ваш заказ принят в очередь'
        return 'wait inqueue', message, None

    def bot_inqueue(text):
        wait_start_cook(update.message.from_user.id, menu_data.order)
        message = 'Мы начали готовить ваш заказ.'
        return 'start cook', message, None

    def bot_start_cook(text):
        wait_end_cook(update.message.from_user.id, menu_data.order)
        wait_for_alarm(update.message.from_user.id)
        message = 'Ваш заказ готов.'
        return 'end cook', message, None

    def bot_end_cook(text):
        # wait_end_cook(update.message.from_user.id, menu_data.order)
        wait_for_alarm(update.message.from_user.id)        
        return 'save order', None, None

    def bot_alarm(time,text):
        def alarm(text):
            status = wait_end_order(update.message.from_user.id, time, menu_data.order)
            message = 'Ваш заказ был приготовлен ' + str(time) +  ' минут назад.'
            if status == True:
                return 'end order', message, None
            return 'save order', message, None
        return alarm

    def bot_end_order(text):

        message = 'Спасибо за ваш заказ! \n Выберите продукт:'
        keys = self.menu_data.menu.get_item_names()
        return 'return', message, keys

    def bot_blacklist(time):
        def blacklist():
            status = wait_end_order(update.message.from_user.id, time, meanu_data.order)
            if status == True:
                return 'end order', None, None
            return 'lost order',  'Вы не забрали ваш заказ (', None
        return blacklist

    def bot_banned(time):
        return 'unbanned', None, None

    def go(self,text):
        next,message,keys = self.cur_node.feedback(self, text)
        self.cur_node = self.cur_node.go(next)
        return message, keys


