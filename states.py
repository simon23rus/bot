class Node:
    def __init__(self, name):
        self.map = {}
        self.name = name

    def add_adj(self, message, node):
        self.map[message] = node

    def go(self, message):
        return self.map.get(message, self.map.get(''))

class Graph:

    def __init__(self, cur_node_name):
        self.nodes = {}

        init = self.add_node('init')
        choose = self.add_node('choose')
        make_order = self.add_node('make_order')
        start_cook = self.add_node('start_cook')
        end_cook = self.add_node('end_cook')
        alarm1 = self.add_node('alarm1')
        alarm2 = self.add_node('alarm2')
        blacklist = self.add_node('blacklist')
        banned = self.add_node('banned')

        self.add_edge(init, choose, 'start choosing')
        self.add_edge(choose, make_order, 'verify order')
        self.add_edge(make_order, start_cook, 'start cook')
        self.add_edge(start_cook, end_cook, 'end cook')
        self.add_edge(end_cook, choose, 'end order')
        self.add_edge(alarm1, choose, 'end order')
        self.add_edge(alarm2, choose, 'end order')
        self.add_edge(end_cook, alarm1, 'save order')
        self.add_edge(alarm1, alarm2, 'save order')
        self.add_edge(alarm2, blacklist, 'lost order')
        self.add_edge(blacklist, banned, 'ban')
        self.add_edge(blacklist, choose, 'decrease loyalty')
        self.add_edge(banned, choose, 'increase loyalty')

        self.cur_node = self.nodes[cur_node_name]

    def add_node(self, name):
        node = Node(name)
        self.nodes[name] = node
        return node

    def add_edge(self, src, dst, message):
        src.add_adj(message, dst)

    def go(self, msg):
        self.cur_node = self.cur_node.go(msg)
        return self.cur_node.name



