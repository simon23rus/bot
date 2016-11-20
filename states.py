# -*- coding: utf-8 -*-

import time
import parse_utils
import messages
import random

class Node:
    def __init__(self, name, body_function):
        self.map = {}
        self.name = name
        self.body_function = body_function

    def add_transition(self, message, node):
        self.map[message] = node

    def go(self, message):
        return self.map.get(message, self.map[u'unrecognized'])


class Graph:
    def __init__(self, telegram_id):
        print(u'Graph.__init__() + 1')
        self.menu = None
        self.last_item_name = None
        self.order = None
        self.nodes = {}
        self.telegram_id = str(telegram_id)
        parse_utils.init_parse()
        parse_utils.create_user(self.telegram_id)
        print(u'Graph.__init__() + 2')

        self.add_node(u'show_menu', self.show_menu)
        self.add_node(u'confirm_order', self.confirm_order)
        self.add_node(u'receive_confirmation', self.receive_confirmation) 
        self.add_node(u'wait_in_queue', self.wait_in_queue)
        self.add_node(u'pick_order', self.pick_order)
        self.add_node(u'something_wrong', self.something_wrong)
        print(u'Graph.__init__() + 3')

        for _, node in self.nodes.items():
            node.add_transition(u'unrecognized', self.nodes[u'something_wrong'])
            node.add_transition(u'start_over', self.nodes[u'show_menu'])
        print(u'Graph.__init__() + 4')

        self.add_transition(u'show_menu', u'confirm_order', u'')
        self.add_transition(u'confirm_order', u'receive_confirmation', u'')
        self.add_transition(u'receive_confirmation', u'wait_in_queue', u'yes')
        self.add_transition(u'receive_confirmation', u'show_menu', u'no')
        self.add_transition(u'wait_in_queue', u'wait_in_queue', u'in_queue')
        self.add_transition(u'wait_in_queue', u'pick_order', u'processed')
        self.add_transition(u'pick_order', u'pick_order', u'not_picked')
        self.add_transition(u'pick_order', u'show_menu', u'picked')
        self.add_transition(u'something_wrong', u'show_menu', u'')
        print(u'Graph.__init__() + 5')

        self.cur_node = self.nodes[u'show_menu']


    def reset_vars(self):
        self.menu = None
        self.last_item_name = None
        self.order = None

    def add_node(self, name, fun):
        node = Node(name, fun)
        self.nodes[name] = node
        return node

    def add_transition(self, from_state, to_state, message):
        self.nodes[from_state].add_transition(message, self.nodes[to_state])

    def go(self, text):
        print(u'go-1')
        transition, message, keys = self.cur_node.body_function(text)
        print(u'nnn: "', transition, u'", message: "', message, u'", keys : "', keys, u'"')
        print(u'go-2')
        self.cur_node = self.cur_node.go(transition)
        print(u'go_3')
        return message, keys

    #
    # Body Functions which are triggered when we get to the corresponding Node
    #
    def show_menu(self, text):
        self.menu = parse_utils.Menu()
        menu_items = [[item] for item in self.menu.get_item_names()]
        return u'', messages.choose_item, menu_items

    def confirm_order(self, text):
        if not text in self.menu.get_item_names():
            return u'unrecognized', u'', []
        self.last_item_name = text
        keys = [[messages.yes], [messages.no]]
        return u'', messages.confirm_question.format(text), keys

    def receive_confirmation(self, text):
        if text == messages.yes:
            self.order = self.menu.place_order_by_name(self.telegram_id, self.last_item_name)
            return u'yes', messages.confirm_order, []
        elif text == messages.no:
            self.reset_vars()
            return u'no', u'', []
        else:
            return u'unrecognized', u'', []

    def wait_in_queue(self, text):
        if self.order.in_queue():
            print("Order still in a queue")
            # time.sleep(1)
            print("returning")
            return u'in_queue', u'', []
        else:
            print("Now I can pick")
            return u'processed', messages.ready_to_pick, []

    def pick_order(self, text):
        if self.order.picked():
            return u'picked', random.choice(messages.bon_appetit), []
        else:
            return u'not_picked', '', []

    def something_wrong(self, text):
        self.reset_vars()
        return u'start_over', messages.something_wrong, []
