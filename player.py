#!/usr/bin/env python3
import random
import numpy as np

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """
        alpha_top = -9999
        beta_top = 9999

        # create children node
        initial_tree_node.compute_and_get_children()
        #print(len(children))  # equals 5

        depth_limit = 2  #depth limit in minimax search

        best_score = -9999
        best_score = self.minimax(initial_tree_node, alpha_top, beta_top, depth_limit)

        print(best_score)

        #function()# returning the best move

        random_move = random.randrange(5)
        return ACTION_TO_STR[random_move]

    def minimax(self, node: Node, alpha, beta, depth_limit):
        if node.depth == depth_limit:
            return self.heuristic(node)
        alpha = -999
        beta = 999


        if not (node.state.get_player == 0): #MIN's turn
            best_value = 999
            #children = node.compute_and_get_children()
            for i in node.children:
                value = self.minimax(i, alpha, beta, depth_limit)
                
                best_value = min(value, best_value)'
                
                beta = min(best_value, beta)
                if beta <= alpha:
                    break
            #return min_value

        else:  # MAX's turn
            best_value = -999
            #children = node.compute_and_get_children()
            for i in node.children:
                value = self.minimax(i, alpha, beta, depth_limit)
                best_value = max(value, best_value)
                alpha = max(best_value, alpha)
                if beta <= alpha:
                     break
        return best_value 

    def heuristic(self, node: Node):  #given a node, return a heuristic value

        hook_pos = node.state.get_hook_positions # return: dict of 2-tuples with (x, y) values of each player's hook
        fish_pos = node.state.get_fish_positions
        #print(fish_pos()[0])
        print("fish position at:" , fish_pos()) # maybe here can compute the avergae of fish
        #print(np.average(fish_pos().values()))
        x_sum = 0
        y_sum = 0
        for i in range(len(fish_pos().keys())):
            x_sum = x_sum + fish_pos()[i][0]
            y_sum = y_sum + fish_pos()[i][1]
        average_xy = (x_sum/len(fish_pos().keys()), y_sum/len(fish_pos())) #to get the average position of all the fishes
        
        dist = np.sqrt((hook_pos[0] - average_xy[0])^2 + (hook_pos[1] - average_xy[1])^2)
        value = -dist # we want to stay close to the fishes
        #hook_pos()[0]
        return value
