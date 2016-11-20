# -*- coding: utf-8 -*-

import parse_utils
import messages


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
    def __init__(self, telegram_id, alarm_time=[5, 10, 15]):
        parse_utils.init_parse()
        parse_utils.create_user(self.telegram_id)

        self.menu = None
        self.last_item_name = None
        self.order = None
        self.nodes = {}
        self.telegram_id = telegram_id

        self.add_node(u'show_menu', self.show_menu)
        self.add_node(u'confirm_order', self.confirm_order)
        self.add_node(u'wait_in_queue', self.wait_in_queue)
        self.add_node(u'pick_order', self.pick_order)
        self.add_node(u'something_wrong', self.something_wrong)

        for _, node in self.nodes.items():
            node.add_transition(u'unrecognized', self.nodes[u'something_wrong'])
            node.add_transition(u'start_over', self.nodes[u'show_menu'])

        self.add_transition(u'show_menu', u'confirm_order', '')
        self.add_transition(u'confirm_order', u'wait_in_queue', '')
        self.add_transition(u'wait_in_queue', u'pick_order', '')
        self.add_transition(u'pick_order', u'show_menu', '')
        self.add_transition(u'something_wrong', u'show_menu', '')

        # self.add_node('init', self.bot_init)
        # self.add_node('choose', self.bot_choose)
        # self.add_node('make_order', self.bot_make_order)
        # self.add_node('inqueue', self.bot_inqueue)
        # self.add_node('start_cook', self.bot_start_cook)
        # self.add_node('end_cook', self.bot_end_cook)
        # self.add_edge('init', 'choose', 'start choosing')
        # self.add_edge('choose', 'make_order', 'verify order')
        # self.add_edge('make_order', 'choose', 'return')
        # self.add_edge('make_order', 'inqueue', 'wait inqueue')
        # self.add_edge('inqueue', 'start_cook', 'start cook')
        # self.add_edge('start_cook', 'end_cook', 'end cook')

        self.cur_node = self.nodes[u'show_menu']

        # self.add_edge(end_order, choose, 'return')

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
        next_node_name, message, keys = self.cur_node.body_function(text)
        self.cur_node = self.cur_node.go(next_node_name)
        return message, keys

    #
    # Body Functions which are triggered when we get to the corresponding Node
    #
    def show_menu(self, text):
        self.menu = parse_utils.Menu()
        return u'', messages.choose_item, self.menu.get_item_names()

    def confirm_order(self, text):
        if not text in self.menu.get_item_names():
            return u'unrecognized', u'', []
        self.last_item_name = text
        keys = [messages.yes, messages.no]
        return u'', messages.confirm_question.format(text), keys

    def wait_in_queue(self, text):
        if text == messages.yes:
            self.order = self.menu.place_order_by_name(self.last_item_name)
            return u'', messages.confirm_order, []
        elif text == messages.no:
            self.reset_vars()
            return u'start_over', u'', []
        else:
            return u'unrecognized', u'', []

    def pick_order(self, text):
        return u'', messages.ready_to_pick, []

    def something_wrong(self, text):
        return u'start_over', messages.something_wrong, []
