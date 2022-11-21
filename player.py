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
        alpha_top = np.NINF
        beta_top = np.PINF
        children = initial_tree_node.compute_and_get_children()
        best_score = np.NINF
        for i in children:
            current_score = self.minimax(i, alpha_top, beta_top)
            if current_score > best_score:
                best_score = current_score

        print(best_score)
        #but it needs to return the action

        random_move = random.randrange(5)
        return ACTION_TO_STR[random_move]

    def minimax(self, alpha, beta):
        alpha = np.NINF
        beta = np.PINF
        depth = 2
        current_turn = node.state.getplayer()

        if current_turn > 0:
            min_value = np.PINF
            children = node.compute_and_get_children()
            for i in children:
                value = self.minimax(i, alpha, beta)
                min_value = min(value, min_value)
                beta = min(min_value, beta)
                # if beta <= alpha:
                #     break
            return min_value

        else:
            max_value = np.NINF
            children = node.compute_and_get_children()
            for i in children:
                value = self.minimax(i, alpha, beta)
                max_value = max(value, max_value)
                alpha = max(max_value, alpha)
                # if beta <= alpha:
                #     break
            return max_value
        
        

