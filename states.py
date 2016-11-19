from handlers import *
from process_orders import *

class Node:
    def __init__(self, name, feedback):
        self.map = {}
        self.name = name
        self.feedback = feedback

    def add_adj(self, message, node):
        self.map[message] = node

    def go(self, message):
        return self.map.get(message, self.map.get(''))

class Graph:
    def __init__(self, cur_node_name, bot, update, menu, alarm_time = [5,10,15]):
        self.nodes = {}
        self.bot = bot
        self.menu = menu
        self.update = update
        self.order = None

        init = self.add_node('init', bot_init)
        choose = self.add_node('choose', bot_choose)
        make_order = self.add_node('make_order', bot_make_order)
        inqueue = self.add_node('inqueue', bot_inqueue)
        start_cook = self.add_node('start_cook', bot_start_cook)
        end_cook = self.add_node('end_cook', bot_end_cook)
        alarm1 = self.add_node('alarm1', bot_alarm(alarm_time[0]))
        alarm2 = self.add_node('alarm2', bot_alarm(alarm_time[1]))
        blacklist = self.add_node('blacklist', bot_blacklist(alarm_time[2]))
        banned = self.add_node('banned', bot_banned)
        end_order = self.add_node('end_order', bot_end_order)

        self.add_edge(init, choose, 'start choosing')
        self.add_edge(choose, make_order, 'verify order')
        self.add_edge(make_order, inqueue, 'wait inqueue')
        self.add_edge(inqueue, start_cook, 'start cook')
        self.add_edge(start_cook, end_cook, 'end cook')
        self.add_edge(end_cook, choose, 'end order')
        self.add_edge(alarm1, end_order, 'end order')
        self.add_edge(alarm2, end_order, 'end order')
        self.add_edge(end_cook, alarm1, 'wait getting')
        self.add_edge(alarm1, alarm2, 'save order')
        self.add_edge(alarm2, blacklist, 'save order')
        self.add_edge(blacklist, banned, 'ban')
        self.add_edge(blacklist, choose, 'lost order')
        self.add_edge(banned, choose, 'unbanned')
        self.add_edge(end_order, choose, 'return')

        self.cur_node = self.nodes[cur_node_name]

    def add_node(self, name):
        node = Node(name)
        self.nodes[name] = node
        return node

    def add_edge(self, src, dst, message):
        src.add_adj(message, dst)

    def go(self):
        msg = self.cur_node.feedback(self, self.bot, self.update, self.menu, self.order)
        self.cur_node = self.cur_node.go(msg)

def run_graph(bot, update):
    init_parse()
    menu = Menu()
    graph = Graph('init', bot, update)
    while True:
        graph.go()

