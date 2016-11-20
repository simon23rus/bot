#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time

from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User

import parse_config


class User(Object):
    pass


class Order(Object):
    pass


class Product(Object):
    pass


def create_user(telegram_id):
    users = User.Query.filter(telegramId=telegram_id)
    if len(users) == 0:
        user = User()
        user.telegramId = telegram_id
        user.save()

class MenuItem(object):
    def __init__(self, menu_id, product):
        self.menu_id = menu_id
        self.name = product.name
        self.price = product.price
        self.parse_id = product.objectId

    def to_unicode(self):
        return u'{}. {} - {}'.format(self.menu_id, self.name, self.price)

    def __str__(self):
        return self.to_unicode()

    def __repl__(self):
        return self.to_unicode()


class MenuOrder(object):
    def __init__(self, parse_order):
        self.parse_order = parse_order

    def update(self):
        self.parse_order = Order.Query.get(objectId=self.parse_order.objectId)

    def get_status(self):
        self.update()
        return self.parse_order.status

    def cancel(self):
        self.parse_order.status = u'CANCELLED'
        self.parse_order.save()

    def in_queue(self):
        orders = Order.Query.filter(objectId=self.parse_order.objectId)
        return len(orders) == 1
    
    def picked(self):
        time.sleep(2)
        return True

    def wait_status(self, status, wait_time=10 ** 2):
        passed_time = 0
        while self.get_status() != status and passed_time < wait_time:
            time.sleep(1)
            wait_time += 1
        return self.parse_order.status == status


class Menu(object):
    def __init__(self):
        products = Product.Query.all()
        self.items = []
        for menu_id, product in enumerate(products, start=1):
            self.items.append(MenuItem(menu_id, product))

    def text(self):
        menu_string = u''
        for item in self.items:
            menu_string += item.to_unicode() + u'\n'
        return menu_string

    def get_item_names(self):
        item_names = []
        for item in self.items:
            item_names.append(item.name)
        return item_names

    def place_order_by_name(self, telegram_id, menu_name):
        item = next(item for item in self.items if item.name == menu_name)
        return self.place_order(telegram_id, item.menu_id)

    def place_order(self, telegram_id, menu_id):
        item = next(item for item in self.items if item.menu_id == menu_id)
        user = User.Query.get(telegramId=telegram_id)
        product = Product.Query.get(objectId=item.parse_id)

        order = Order()
        order.status = u'IN_QUEUE'
        order.save()
        order.productId = product.objectId
        order.userId = user.objectId
        order.save()
        return MenuOrder(order)


def init_parse():
    register(parse_config.application_key, parse_config.rest_api_key, master_key=parse_config.master_key)


def place_bunch_orders():
    init_parse()
    menu = Menu()
    for i in range(10):
        order = menu.place_order(u'Danchik', 1)


def test():
    init_parse()
    menu = Menu()
    print(menu.text())
    order = menu.place_order(u'Danchik', 1)
    name = menu.get_item_names()[3]
    order_2 = menu.place_order_by_name(u'Migelio', name)
    print(order)
    while order.in_queue():
        print(u'Processing')
    print(u'DONE!')


if __name__ == u'__main__':
    test()
