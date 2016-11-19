# -*- coding: utf-8 -*-

from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User
import parse_config as config
import time


class User(Object):
    pass


class Order(Object):
    pass


class Product(Object):
    pass


def create_user(telegram_id):
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

    # returns one of : 'IN_QUEUE', 'CANCELLED', 'PROCESSING', 'DONE', 'PICKED'
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

    def place_order(self, telegram_id, menu_id):
        item = next(item for item in self.items if item.menu_id == menu_id)
        user = User.Query.get(telegramId=telegram_id)
        product = Product.Query.get(objectId=item.parse_id)

        order = Order()
        order.status = u'IN_QUEUE'
        order.save()
        order.relation('product').add(product)
        order.relation('user').add(user)
        order.save()
        return MenuOrder(order)


def init_parse():
    register(config.application_key, config.rest_api_key, master_key=config.master_key)


def place_bunch_orders():
    init_parse()
    menu = Menu()
    for i in range(10):
        order = menu.place_order('Danchik', 1)

def test():
    init_parse()
    menu = Menu()
    print(menu.text())
    order = menu.place_order('Danchik', 1)
    print(order)
    while order.in_queue():
        print('Processing')
    print('DONE!')


if __name__ == "__main__":
    place_bunch_orders()
    test()
