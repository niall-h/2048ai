from __future__ import absolute_import, division, print_function
import copy, random
import math

from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1


# Tree node. To construct a game tree. 
class Node:
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return not self.children

    def get_state(self):
        return self.state


# AI agent. Determine the next move.
class AI:
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)


    def build_tree(self, node=None, depth=0):
        if depth >= 0:
            if not node.player_type:  # MAX_PLAYER = 0
                for move in MOVES:
                    self.simulator.set_state(node.get_state()[0], node.get_state()[1])
                    if self.simulator.move(move):
                        child_node = Node(self.simulator.current_state(), CHANCE_PLAYER)
                        node.children.append(child_node)
                        self.build_tree(child_node, depth - 1)
                    else:
                        node.children.append(Node(self.simulator.current_state(), 2))
            elif node.player_type:  # CHANCE_PLAYER = 1
                open_tiles = self.simulator.get_open_tiles()
                for (i, j) in open_tiles:
                    self.simulator.set_state(node.get_state()[0], node.get_state()[1])
                    self.simulator.tile_matrix[i][j] = 2
                    child_node = Node(self.simulator.current_state(), MAX_PLAYER)
                    node.children.append(child_node)
                    self.build_tree(child_node, depth - 1)
                    self.simulator.set_state(node.get_state()[0], node.get_state()[1])

    def expectimax(self, node=None):
        if node.player_type == 2:
            return 5, 0
        elif node.is_terminal():
            return 0, node.state[1]
        elif not node.player_type:
            value = -math.inf
            direction = 0
            for index, child in enumerate(node.children):
                new_value = max(value, self.expectimax(child)[1])
                if new_value != value:
                    direction = index
                    value = new_value
            return direction, value
        elif node.player_type:
            value = 0
            for child in node.children:
                print(len(node.children))
                value = value + self.expectimax(child)[1] * (1 / len(node.children))
            return 5, value

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction